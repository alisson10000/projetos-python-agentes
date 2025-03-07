import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Carregar variáveis do ambiente (.env)
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

# API Keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verificação das chaves de API
if not OPENWEATHER_API_KEY or not OPENAI_API_KEY:
    raise ValueError("⚠️ Erro: As chaves da API não foram carregadas corretamente. Verifique seu arquivo .env!")

# Configuração do modelo de IA
modelo = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

def extrair_cidade_com_ia(pergunta):
    """Usa IA para identificar e extrair apenas o nome da cidade."""

    prompt_ia = f"""
    Extraia **apenas** o nome da cidade da seguinte frase: '{pergunta}'.
    Ignore palavras como 'qual a previsão', 'clima', 'tempo', 'vai chover', 'de', 'em', 'para', 'agora'.
    Retorne **somente** o nome da cidade, sem nenhuma explicação ou palavras extras.
    Se não houver cidade na pergunta, retorne 'NENHUMA'.
    """

    try:
        resposta_ia = modelo.invoke(prompt_ia).content.strip()
    except Exception as e:
        return f"Erro ao processar a cidade com IA: {e}"

    # Retorna None se a IA não conseguir encontrar uma cidade
    return None if resposta_ia.lower() in ["nenhuma", "erro"] else resposta_ia

def obter_previsao_tempo(pergunta):
    """Obtém a previsão do tempo para uma cidade usando OpenWeatherMap."""

    # Extraindo a cidade usando IA
    cidade = extrair_cidade_com_ia(pergunta)

    if not cidade:
        return "⚠️ Por favor, informe corretamente o nome da cidade. Exemplo: 'Qual a previsão do tempo em São Paulo?'" 

    # Construindo a URL corretamente
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pt"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"🚨 Erro ao acessar a API de clima: {e}"

    if data.get("cod") != 200:
        return f"⚠️ Erro: {data.get('message', 'Não foi possível obter a previsão do tempo.')}"

    # Extraindo informações do JSON corretamente
    temperatura = data["main"]["temp"]
    descricao = data["weather"][0]["description"].capitalize()
    sensacao = data["main"]["feels_like"]
    umidade = data["main"]["humidity"]
    vento = data["wind"]["speed"]

    resposta = (
        f"🌦️ **Previsão do tempo para {cidade.title()}**:\n"
        f"🌡️ **Temperatura:** {temperatura}°C\n"
        f"🤒 **Sensação térmica:** {sensacao}°C\n"
        f"☁️ **Condição:** {descricao}\n"
        f"💧 **Umidade:** {umidade}%\n"
        f"💨 **Vento:** {vento} m/s"
    )

    return resposta

# Teste simples
if __name__ == "__main__":
    while True:
        pergunta = input("\nVocê: ")
        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando...")
            break
        
        resposta = obter_previsao_tempo(pergunta)
        print("\n🌍 Agente do Clima:", resposta)
