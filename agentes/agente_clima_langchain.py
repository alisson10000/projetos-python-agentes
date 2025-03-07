import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict
from clima_langchain import obter_previsao_tempo  # Função que busca a previsão do tempo

# 🔹 Carregar variáveis do ambiente (.env) contendo as chaves das APIs
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Validação da chave de API para evitar erros na execução
if not OPENAI_API_KEY:
    print("⚠️ Erro: A API Key da OpenAI não foi encontrada! Verifique o arquivo .env.")
    exit(1)

# 🔹 Criando o modelo de IA utilizando a API da OpenAI via LangChain
modelo = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

# 🔹 Criando a Memória Persistente para manter o histórico da conversa
memoria = ChatMessageHistory()

# 🔹 Criando um prompt personalizado para o agente, permitindo a integração do histórico da conversa
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Você é um assistente útil e amigável. Se perguntarem sobre o tempo, consulte a API de clima."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{question}")  # Placeholder para a pergunta do usuário
])

# 🔹 Definição da estrutura do estado do agente usando TypedDict
class AgentState(TypedDict):
    chat_history: ChatMessageHistory  # Histórico das interações do usuário com o agente
    question: str                     # Pergunta atual do usuário
    response: str                      # Resposta gerada pelo agente

# 🔹 Criando um fluxo de execução para o agente usando LangGraph
workflow = StateGraph(AgentState)

# 🔹 Função principal do agente para processar perguntas e gerar respostas
def processar_pergunta(state: AgentState) -> Dict:
    """Processa a entrada do usuário, identifica se é uma consulta sobre clima ou um diálogo geral, 
    mantém o histórico e gera respostas adequadas."""

    pergunta_usuario = state["question"].lower()

    # ✅ 🔍 Verifica se a pergunta está relacionada ao clima usando palavras-chave comuns
    if any(palavra in pergunta_usuario for palavra in ["tempo", "previsão", "clima", "vai chover", "chuva", "sol", "temperatura"]):
        resposta_clima = obter_previsao_tempo(state["question"])  # Chama a API de previsão do tempo
        return {"chat_history": memoria, "question": state["question"], "response": resposta_clima}

    # ✅ 🔍 Se não for uma consulta sobre clima, a IA responde normalmente
    mensagens = memoria.messages + [HumanMessage(content=state["question"])]  # Atualiza o histórico com a nova pergunta

    # ✅ 🔍 Gera uma resposta baseada no contexto da conversa
    resposta = modelo.invoke(mensagens)

    # ✅ 🔍 Armazena a interação na memória para manter a continuidade do diálogo
    memoria.add_user_message(state["question"])
    memoria.add_ai_message(resposta.content)

    # Retorna o novo estado atualizado contendo a resposta
    return {"chat_history": memoria, "question": state["question"], "response": resposta.content}

# 🔹 Adicionando estados ao fluxo do LangGraph
workflow.add_node("responder", processar_pergunta)  # Define o nó de resposta
workflow.set_entry_point("responder")  # Define o ponto de entrada no fluxo
workflow.add_edge("responder", END)  # Define a transição final do fluxo

# 🔹 Compilando o fluxo do agente para ser executado
agente = workflow.compile()

def iniciar_chat():
    """Inicia a interação do usuário com o agente de IA, permitindo perguntas gerais e consultas sobre clima,
    com suporte a memória de contexto e histórico da conversa."""

    print("✅ Agente Inteligente com LangGraph iniciado! (Versão Final)")
    print("Digite 'sair' para encerrar ou 'limpar' para resetar a memória.\n")

    while True:
        pergunta = input("Você: ")

        # ✅ 🔍 Verifica se o usuário quer encerrar o chat
        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando o agente...")
            break
        
        # ✅ 🔍 Verifica se o usuário quer limpar a memória
        elif pergunta.lower() in ["limpar", "resetar"]:
            memoria.clear()
            print("🧠 Memória apagada! O agente esqueceu a conversa anterior.")
            continue

        # ✅ 🔍 Processa a pergunta do usuário e obtém a resposta do agente
        resposta = agente.invoke({"chat_history": memoria, "question": pergunta})

        # ✅ 🔍 Exibe a resposta do agente ou um aviso em caso de erro
        if "response" in resposta:
            print("Agente:", resposta["response"])
        else:
            print("⚠️ Erro: A resposta não foi gerada corretamente.")

# 🔹 Executa o agente no terminal quando o script for executado diretamente
if __name__ == "__main__":
    iniciar_chat()
