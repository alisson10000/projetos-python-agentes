import openai
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

# Obtém a chave da API
API_KEY = os.getenv("OPENAI_API_KEY")

# Configuração do cliente OpenAI
client = openai.OpenAI(api_key=API_KEY)

# Classe do Agente IA
class AgenteIA:
    def __init__(self, modelo="gpt-4"):
        self.modelo = modelo
        self.historico = []  # Memória do agente

    def interagir(self, pergunta):
        # Adiciona a pergunta ao histórico
        self.historico.append({"role": "user", "content": pergunta})

        # Envia a mensagem para a IA
        resposta = client.chat.completions.create(
            model=self.modelo,
            messages=self.historico
        )

        # Obtém a resposta da IA
        resposta_texto = resposta.choices[0].message.content

        # Adiciona a resposta ao histórico
        self.historico.append({"role": "assistant", "content": resposta_texto})

        return resposta_texto

# Testando o agente
if __name__ == "__main__":
    agente = AgenteIA()  # Criando um agente com GPT-4
    while True:
        pergunta = input("Você: ")
        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando o agente...")
            break
        resposta = agente.interagir(pergunta)
        print("Agente:", resposta)
