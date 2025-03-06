import requests
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# API Key da WeatherAPI
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")

def obter_previsao_tempo(pergunta):
    """Analisa a pergunta e obtém a previsão do tempo para uma cidade usando WeatherAPI."""
    
    # Lista de palavras-chave para identificar a cidade
    palavras = pergunta.split()
    cidade = None
    
    # Tenta identificar o nome da cidade na pergunta
    for i in range(len(palavras)):
        if palavras[i].lower() in ["em", "para", "de"]:  # Exemplo: "Como está o tempo em São Paulo?"
            cidade = " ".join(palavras[i+1:])
            break
    
    # Se não encontrou a cidade, pede ao usuário para especificar
    if not cidade:
        return "Por favor, informe a cidade. Exemplo: 'Qual a previsão do tempo em São Paulo?'"

    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={cidade}&lang=pt"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a API de clima: {e}"

    if "error" in data:
        return f"Erro: {data['error']['message']}"

    # Extrair informações do JSON
    temperatura = data["current"]["temp_c"]
    descricao = data["current"]["condition"]["text"]
    sensacao = data["current"]["feelslike_c"]
    umidade = data["current"]["humidity"]

    resposta = (f"🌡️ **Previsão do tempo para {cidade.title()}**:\n"
                f"- Temperatura: {temperatura}°C\n"
                f"- Sensação térmica: {sensacao}°C\n"
                f"- Condição: {descricao}\n"
                f"- Umidade: {umidade}%")

    return resposta
