import openai
import os
from dotenv import load_dotenv

# Carregar variáveis do ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verificação da chave da API
if not OPENAI_API_KEY:
    print("⚠️ Erro: A API Key da OpenAI não foi encontrada! Verifique o arquivo .env.")
    exit(1)

# Configuração do cliente OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class AgenteInteligente:
    def __init__(self):
        self.memoria = []  # Lista para armazenar histórico da conversa

    def adicionar_memoria(self, usuario, agente):
        """Adiciona mensagens ao histórico da conversa."""
        self.memoria.append({"role": "user", "content": usuario})
        self.memoria.append({"role": "assistant", "content": agente})

    def conversar(self, pergunta):
        """Processa a pergunta e responde mantendo o contexto."""

        # Adicionar histórico da conversa
        mensagens = [{"role": "system", "content": "Você é um assistente inteligente e amigável."}]
        mensagens.extend(self.memoria)  # Adiciona o histórico da conversa
        mensagens.append({"role": "user", "content": pergunta})

        try:
            resposta = client.chat.completions.create(
                model="gpt-4",
                messages=mensagens
            )
            resposta_texto = resposta.choices[0].message.content

            # Armazena a conversa na memória
            self.adicionar_memoria(pergunta, resposta_texto)

            return resposta_texto
        except Exception as e:
            return f"Erro ao acessar a OpenAI: {e}"

    def resetar_memoria(self):
        """Reseta a memória da conversa."""
        self.memoria = []
        return "Memória apagada! O agente esqueceu a conversa anterior."

# Testando o agente
if __name__ == "__main__":
    print("✅ Agente Inteligente iniciado!")

    agente = AgenteInteligente()

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando o agente...")
            break
        elif pergunta.lower() in ["limpar", "resetar"]:
            print(agente.resetar_memoria())
            continue

        resposta = agente.conversar(pergunta)
        print("Agente:", resposta)
