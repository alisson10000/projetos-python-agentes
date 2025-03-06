import os
import requests
import json
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

# Chaves de API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# Verificação das chaves de API antes de iniciar o agente
if not GEMINI_API_KEY:
    print("⚠️ Erro: A API Key do Gemini não foi encontrada! Verifique o arquivo .env.")
    exit(1)

if not GNEWS_API_KEY:
    print("⚠️ Erro: A API Key da GNews não foi encontrada! Verifique o arquivo .env.")
    exit(1)

# URL correta da API do Gemini 2.0 Flash
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

class AgenteIA:
    def __init__(self):
        self.historico = []
        self.iniciar_personalidade()

    def iniciar_personalidade(self):
        """Define a personalidade inicial do agente"""
        self.historico.append({
            "role": "system",
            "content": "Você é um assistente amigável e útil. Se perguntarem sobre notícias, consulte a API de notícias."
        })

    def interagir(self, pergunta):
        """Processa a pergunta e gera uma resposta"""

        # Responde ao "bom dia" trazendo notícias
        if "bom dia" in pergunta.lower():
            return "Bom dia! Aqui estão as últimas notícias:\n\n" + self.buscar_noticias()

        # Responde ao "boa noite" trazendo as principais notícias do dia
        if "boa noite" in pergunta.lower():
            return "Boa noite! Aqui estão as principais notícias de hoje:\n\n" + self.buscar_noticias()

        # Chamando função buscar_noticias() para qualquer pergunta sobre notícias
        if "notícias" in pergunta.lower() or "news" in pergunta.lower():
            return self.buscar_noticias()

        self.historico.append({"role": "user", "content": pergunta})

        try:
            resposta = self.chamar_gemini(pergunta)
        except Exception as e:
            return f"Erro ao acessar a API Gemini: {e}"

        self.historico.append({"role": "assistant", "content": resposta})

        return resposta

    def chamar_gemini(self, pergunta):
        """Faz uma requisição à API do Gemini e retorna a resposta"""

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "contents": [{
                "parts": [{"text": pergunta}]
            }]
        }

        try:
            response = requests.post(GEMINI_URL, headers=headers, json=data)
            response.raise_for_status()
            resposta_json = response.json()

            # Extração da resposta corretamente
            candidates = resposta_json.get("candidates", [])
            if candidates:
                content_parts = candidates[0].get("content", {}).get("parts", [])
                if content_parts:
                    return content_parts[0].get("text", "Erro: Nenhuma resposta gerada.")
                else:
                    return "Erro: Resposta vazia da API."
            else:
                return "Erro: Nenhuma resposta encontrada na API."

        except requests.exceptions.RequestException as e:
            return f"Erro na requisição à API Gemini: {e}"

    def buscar_noticias(self):
        """Busca as últimas notícias na GNews"""
        url = f"https://gnews.io/api/v4/top-headlines?token={GNEWS_API_KEY}&lang=pt"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return f"Erro ao acessar a GNews API: {e}"

        if data.get("articles"):
            noticias = data["articles"][:5]  # Pega as 5 principais notícias do dia
            resposta = "Aqui estão as principais notícias do dia:\n\n"
            for noticia in noticias:
                resposta += f"- {noticia.get('title', 'Sem título')} ({noticia.get('source', {}).get('name', 'Fonte desconhecida')})\n  Link: {noticia.get('url', 'Sem link')}\n\n"
            return resposta

        return "Nenhuma notícia recente foi encontrada no momento. Tente novamente mais tarde."

    def resetar_memoria(self):
        """Reseta o histórico do agente"""
        self.historico = []
        self.iniciar_personalidade()

# Testando o agente
if __name__ == "__main__":
    print("✅ Agente IA iniciado com sucesso!")

    agente = AgenteIA()

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando o agente...")
            break
        elif pergunta.lower() in ["resetar", "limpar memória", "esquecer"]:
            agente.resetar_memoria()
            print("Memória apagada! O agente esqueceu a conversa anterior.")
            continue
        elif pergunta.lower() in ["testar notícias", "buscar notícias"]:
            resposta = agente.buscar_noticias()
            print("Agente:", resposta)
            continue

        resposta = agente.interagir(pergunta)
        print("Agente:", resposta)
