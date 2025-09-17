 
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests
import asyncio
from datetime import datetime
import pytz
import aiohttp
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret")
socketio = SocketIO(app)

GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
 
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {GROQ_API_KEY}'
}
 
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
 
chat_atual = None
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    global chat_atual
    chat_atual = None
    return render_template('chat.html')
 
@socketio.on('enviar_mensagem')
def enviar_mensagem(data):
    mensagem = data.get('mensagem')
    global chat_atual
 
    # Payload para gerar o nome do chat
    payload_nome = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": f"Gere um nome de chat de conversa condizente com essa pergunta: {mensagem}. Envie APENAS o nome recomentado, sem nenhuma mensagem adicional."
            }
        ]
    }
 
    try:
        nome_chat = requests.post(GROQ_API_URL, headers=HEADERS, json=payload_nome)
 
        if nome_chat.ok:
            resposta_nome = nome_chat.json()['choices'][0]['message']['content'].strip()
            resposta_nome = resposta_nome.split("\n")[0]  # pega só a primeira linha
        else:
            resposta_nome = f"Erro ao gerar nome: {nome_chat.status_code} - {nome_chat.text}"
    except Exception as e:
        resposta_nome = f"Erro ao gerar nome: {str(e)}"
 
    print("Nome do chat:", resposta_nome)
 
    # Payload para gerar a resposta da IA
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": mensagem
            }
        ]
    }
 
    try:
        response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
 
        if response.ok:
            resposta_ia = response.json()['choices'][0]['message']['content']
            if chat_atual == None:
                chat_atual = resposta_nome
            asyncio.run(registrar_mensagem(chat_atual, mensagem, resposta_ia))
        else:
            resposta_ia = f'Erro na IA: {response.status_code} - {response.text}'
    except Exception as e:
        resposta_ia = f'Erro: {str(e)}'
 
    emit('resposta_webhook', {'resposta': resposta_ia})
 
async def registrar_mensagem(nome, mensagem, resposta):
    # Data formatada para o fuso horário de São Paulo
    fuso = pytz.timezone("America/Sao_Paulo")
    data = datetime.now(fuso).strftime("%d/%m/%Y %H:%M:%S")
 
    url = "https://hook.us2.make.com/w4n4awkgqgarmkac4ek1ybrkebjgeuzf"
    payload = {
        "nome": nome,
        "mensagem": mensagem,
        "resposta": resposta,
        "data": data,
    }
 
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    print("Mensagem registrada:", payload)
                else:
                    erro = await response.text()
                    print("Erro ao registrar mensagem:", erro)
    except Exception as e:
        print("Erro ao registrar pedido:", str(e))
 
if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=80, debug=True)