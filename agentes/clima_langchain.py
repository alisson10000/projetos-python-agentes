import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 🔹 Carregar variáveis do ambiente (.env), onde ficam armazenadas as credenciais sensíveis
# Isso permite que o código funcione sem expor diretamente as chaves da API
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

# 🔹 API Keys carregadas a partir do .env para acessar os serviços externos
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Chave da API do OpenWeatherMap
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Chave da API da OpenAI (GPT-4)

# 🔹 Verificação de segurança para garantir que as chaves foram carregadas corretamente
if not OPENWEATHER_API_KEY or not OPENAI_API_KEY:
    raise ValueError("⚠️ Erro: As chaves da API não foram carregadas corretamente. Verifique seu arquivo .env!")

# 🔹 Inicialização do modelo de IA da OpenAI via LangChain
# Esse modelo será utilizado para interpretar perguntas e extrair informações
modelo = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

def extrair_cidade_com_ia(pergunta):
    """ 
    🔍 Usa IA para identificar e extrair **apenas** o nome da cidade de uma frase.
    
    - O modelo de IA irá ignorar palavras desnecessárias como "qual a previsão", "tempo", "clima", etc.
    - Retorna **somente** o nome da cidade.
    - Se não identificar nenhuma cidade na pergunta, retorna 'NENHUMA'.
    """

    prompt_ia = f"""
    Extraia **apenas** o nome da cidade da seguinte frase: '{pergunta}'.
    Ignore palavras como 'qual a previsão', 'clima', 'tempo', 'vai chover', 'de', 'em', 'para', 'agora'.
    Retorne **somente** o nome da cidade, sem nenhuma explicação ou palavras extras.
    Se não houver cidade na pergunta, retorne 'NENHUMA'.
    """

    try:
        resposta_ia = modelo.invoke(prompt_ia).content.strip()
    except Exception as e:
        return f"Erro ao processar a cidade com IA: {e}"  # Captura erros na IA e retorna como mensagem

    # Caso a IA não reconheça a cidade, retorna None para tratamento adequado
    return None if resposta_ia.lower() in ["nenhuma", "erro"] else resposta_ia


def obter_previsao_tempo(pergunta):
    """ 
    🌤️ Obtém a previsão do tempo para uma cidade específica usando a API do OpenWeatherMap.
    
    - A cidade é extraída utilizando IA para melhorar a precisão.
    - Se nenhuma cidade for identificada, o agente pedirá mais informações.
    - Constrói uma requisição HTTP para obter os dados do clima.
    - Retorna uma string formatada com os dados meteorológicos.
    """

    # 🔹 Extração da cidade usando a IA treinada
    cidade = extrair_cidade_com_ia(pergunta)

    if not cidade:
        return "⚠️ Por favor, informe corretamente o nome da cidade. Exemplo: 'Qual a previsão do tempo em São Paulo?'" 

    # 🔹 Monta a URL da requisição HTTP para buscar os dados meteorológicos
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={OPENWEATHER_API_KEY}&units=metric&lang=pt"

    try:
        response = requests.get(url)  # 🔍 Faz a requisição à API do OpenWeatherMap
        response.raise_for_status()  # Se houver erro na resposta (exemplo: cidade inválida), gera uma exceção
        data = response.json()  # Converte a resposta JSON em um dicionário Python
    except requests.exceptions.RequestException as e:
        return f"🚨 Erro ao acessar a API de clima: {e}"  # Retorna uma mensagem de erro amigável

    # 🔹 Verifica se a API retornou um código de erro específico
    if data.get("cod") != 200:
        return f"⚠️ Erro: {data.get('message', 'Não foi possível obter a previsão do tempo.')}"
    
    # 🔹 Extração das informações do JSON
    temperatura = data["main"]["temp"]  # Temperatura atual
    descricao = data["weather"][0]["description"].capitalize()  # Descrição da condição climática
    sensacao = data["main"]["feels_like"]  # Sensação térmica
    umidade = data["main"]["humidity"]  # Umidade do ar
    vento = data["wind"]["speed"]  # Velocidade do vento

    # 🔹 Resposta formatada para exibir os dados meteorológicos ao usuário
    resposta = (
        f"🌦️ **Previsão do tempo para {cidade.title()}**:\n"
        f"🌡️ **Temperatura:** {temperatura}°C\n"
        f"🤒 **Sensação térmica:** {sensacao}°C\n"
        f"☁️ **Condição:** {descricao}\n"
        f"💧 **Umidade:** {umidade}%\n"
        f"💨 **Vento:** {vento} m/s"
    )

    return resposta


# 🔹 Teste interativo do agente de clima
if __name__ == "__main__":
    while True:
        pergunta = input("\n🗣️ Você: ")
        
        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("🚪 Encerrando...")
            break  # Finaliza o programa
        
        resposta = obter_previsao_tempo(pergunta)  # Processa a pergunta e obtém a resposta
        print("\n🌍 Agente do Clima:", resposta)  # Exibe a previsão do tempo formatada
