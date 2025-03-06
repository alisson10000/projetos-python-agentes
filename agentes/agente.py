import openai
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

# Obtém a chave da API do OpenAI
API_KEY = os.getenv("OPENAI_API_KEY")

# Configuração do cliente OpenAI com a versão atualizada
client = openai.OpenAI(api_key=API_KEY)

# Função para interagir com o ChatGPT
def chat_com_ia(pergunta):
    resposta = client.chat.completions.create(
        model="gpt-4",  # Você pode usar "gpt-3.5-turbo" se preferir
        messages=[{"role": "user", "content": pergunta}]
    )
    return resposta.choices[0].message.content

# Testando o agente
pergunta = input("Pergunte algo ao agente: ")
print("Agente:", chat_com_ia(pergunta))
