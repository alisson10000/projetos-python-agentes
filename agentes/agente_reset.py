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
        self.iniciar_personalidade()

    def iniciar_personalidade(self):
        """Define a personalidade inicial do agente"""
        self.historico.append({
            "role": "system",
            "content": "Você é um assistente amigável e útil. Responda de forma clara e objetiva."
        })

    def interagir(self, pergunta):
        """Processa a pergunta e gera uma resposta"""
        self.historico.append({"role": "user", "content": pergunta})

        resposta = client.chat.completions.create(
            model=self.modelo,
            messages=self.historico
        )

        resposta_texto = resposta.choices[0].message.content
        self.historico.append({"role": "assistant", "content": resposta_texto})

        return resposta_texto

    def resetar_memoria(self):
        """Reseta o histórico do agente"""
        self.historico = []  # Apaga tudo
        self.iniciar_personalidade()  # Reinsere a personalidade inicial

# Testando o agente
if __name__ == "__main__":
    agente = AgenteIA()  # Criando um agente com GPT-4
    while True:
        pergunta = input("Você: ")
        
        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando o agente...")
            break
        elif pergunta.lower() in ["resetar", "limpar memória", "esquecer"]:
            agente.resetar_memoria()
            print("🔄 Memória apagada! O agente esqueceu a conversa anterior.")
            continue  # Volta para a próxima interação sem chamar o agente

        resposta = agente.interagir(pergunta)
        print("Agente:", resposta)
