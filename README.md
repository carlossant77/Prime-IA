# Prime-IA
---
Este repositório contem uma **Inteligência Artificial (Prime IA)** realizada utilizando a API do Groq: https://console.groq.com/home que permite integrar modelos de Inteligência Artificial de alta performance em sistemas, bots, sites e aplicativos. As conversas são armazenadas através da plataforma de automação Make e salvas em uma planilha simples no Google Sheets

# Demonstração Visual 🔎
![inicio](static/assets/index.png)
![pagini](static/assets/inicio.png)
![login1](static/assets/chat.png)
![foto1](static/assets/chat1.png)

# Tecnologias Utilizadas 💻
- **HTML:** Estruturação do Web Chat
- **CSS:** Estilização do Web CHat
- **Python:** Linguagem utilizada para incialização do servidor e navegação por rotas
- **Socket.IO:** Microframework utilizado para comunicação em tempo real com a API de implementação de IA's
- **Make:** Envio de conversas salvas automaticamente para uma planilha
- **Google Sheets:** Tabela de armazenamento de conversas simples

# Pré-Requisitos ⚙
- Python instalado na máquina.
- Biblioteca Flask instalada.
- Instalação do microframework Socket.IO.
- **(DEMAIS REQUISITOS DISPONÍVEIS DENTRO DO ARQUIVO: requirements.txt)**

# GUIA DE UTILIZAÇÃO 📝
- Passo 1: Realizar a instalação do projeto na sua máquina e realizar o download de todas as bibliotecas necessárias.
- Passo 2: Crie a sua própria IA utilizando o link: https://console.groq.com/home. Copie e **GUARDE** a sua chave da API criada, altere o nome do arquivo de "env.example" para --> .env e insira a chave copiada no trecho em que ela é solicitada (Não compartilhe a sua chave da IA com ninguém).
- Passo 3: Inicializar o projeto no terminal python e testar livremente.
- PASSOS ADICIONAIS E OPCIONAIS: A aplicação já funciona corretamente com a execução dos passos 1, 2 e 3, porém, para implementar a automatização de processamento de conversas com a plataforma Make, basta gerar um ambiente com um "webhook" para tratar os dados, e criar uma planilha correspondente no Google Sheets para armazenar. Copie o seu link do webhook e cole na página "run.py" na linha 101.

