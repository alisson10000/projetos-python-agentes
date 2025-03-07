import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict


# Agora importa o módulo do banco de dados corretamente
from db_mariadb import salvar_mensagem, recuperar_historico


# 🔹 Carregar variáveis do ambiente (.env)
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Verificação da chave de API
if not OPENAI_API_KEY:
    print("⚠️ Erro: A API Key da OpenAI não foi encontrada! Verifique o arquivo .env.")
    exit(1)

# 🔹 Criando o modelo de IA utilizando a API da OpenAI via LangChain
modelo = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

# 🔹 Criando a Memória Persistente
memoria = ChatMessageHistory()

# 🔹 Criando o Prompt do Agente
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Você é um assistente amigável que lembra das conversas."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{question}")  # Placeholder para entrada do usuário
])

# 🔹 Definição do Estado do Agente
class AgentState(TypedDict):
    chat_history: ChatMessageHistory
    question: str
    response: str

# 🔹 Criando o Grafo do Agente
workflow = StateGraph(AgentState)

def processar_pergunta(state: AgentState) -> Dict:
    """Processa a entrada do usuário, interage com LangChain e armazena a conversa no MariaDB."""
    
    pergunta_usuario = state["question"]

    # 🔍 Recupera histórico da conversa do banco de dados
    historico = recuperar_historico()

    # 🔹 Adiciona mensagens anteriores do usuário ao contexto
    mensagens = historico + [HumanMessage(content=pergunta_usuario)]

    # 🔹 Obtém resposta da IA
    resposta = modelo.invoke(mensagens)

    # 🔹 Armazena no banco de dados
    salvar_mensagem("user", pergunta_usuario)
    salvar_mensagem("ai", resposta.content)

    return {"chat_history": memoria, "question": pergunta_usuario, "response": resposta.content}

# 🔹 Configuração do LangGraph
workflow.add_node("responder", processar_pergunta)
workflow.set_entry_point("responder")
workflow.add_edge("responder", END)

# 🔹 Compilando o Grafo do Agente
agente = workflow.compile()

def iniciar_chat():
    """Inicia o chat interativo com memória persistente no MariaDB."""
    
    print("✅ Agente Inteligente com LangGraph + MariaDB iniciado!")
    print("Digite 'sair' para encerrar ou 'limpar' para resetar a memória.\n")

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando o agente...")
            break
        elif pergunta.lower() in ["limpar", "resetar"]:
            print("⚠️ Função de limpeza de histórico ainda não implementada!")
            continue

        resposta = agente.invoke({"chat_history": memoria, "question": pergunta})

        if "response" in resposta:
            print("Agente:", resposta["response"])
        else:
            print("⚠️ Erro: A resposta não foi gerada corretamente.")

# 🔹 Executa o agente
if __name__ == "__main__":
    iniciar_chat()
