import openai
import os
import requests
from dotenv import load_dotenv
from clima import obter_previsao_tempo  # Importa a função de clima

# Carrega variáveis do arquivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

# Configuração da API da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class AgenteIA:
    def __init__(self, modelo="gpt-4"):
        self.modelo = modelo
        self.historico = []
        self.iniciar_personalidade()

    def iniciar_personalidade(self):
        """Define a personalidade inicial do agente"""
        self.historico.append({
            "role": "system",
            "content": "Você é um assistente amigável e útil. Se perguntarem sobre previsão do tempo, consulte a API de clima."
        })

    def interagir(self, pergunta):
        """Processa a pergunta e gera uma resposta"""

        # Verifica se a pergunta é sobre o clima
        if any(palavra in pergunta.lower() for palavra in ["tempo", "previsão", "clima", "vai chover"]):
            return obter_previsao_tempo(pergunta)

        self.historico.append({"role": "user", "content": pergunta})

        try:
            resposta = client.chat.completions.create(
                model=self.modelo,
                messages=self.historico
            )
            resposta_texto = resposta.choices[0].message.content
        except Exception as e:
            return f"Erro ao acessar a OpenAI: {e}"

        self.historico.append({"role": "assistant", "content": resposta_texto})

        return resposta_texto

# Testando o agente
if __name__ == "__main__":
    print("✅ Agente IA iniciado!")

    agente = AgenteIA()

    while True:
        pergunta = input("Você: ")
        
        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando o agente...")
            break

        resposta = agente.interagir(pergunta)
        print("Agente:", resposta)
