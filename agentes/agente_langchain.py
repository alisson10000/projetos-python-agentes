import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict

# Carregar variáveis do ambiente (.env)
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verificação da chave da API
if not OPENAI_API_KEY:
    print("⚠️ Erro: A API Key da OpenAI não foi encontrada! Verifique o arquivo .env.")
    exit(1)

# Criando o Modelo de IA com LangChain
modelo = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

# Criando a Memória Persistente com LangGraph
memoria = ChatMessageHistory()

# Criando o Prompt do Agente
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Você é um assistente útil e amigável."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{question}")
])

# Definindo o Estado do Agente para LangGraph
class AgentState(TypedDict):
    chat_history: ChatMessageHistory
    question: str
    response: str

# Criando o Grafo do Agente (LangGraph)
workflow = StateGraph(AgentState)

# Função de Processamento do Agente
def processar_pergunta(state: AgentState) -> Dict:
    """Processa a pergunta e mantém a memória persistente"""
    # Criando histórico formatado para o modelo
    mensagens = memoria.messages + [HumanMessage(content=state["question"])]

    # Gerando resposta
    resposta = modelo.invoke(mensagens)

    # Armazenando na memória
    memoria.add_user_message(state["question"])
    memoria.add_ai_message(resposta.content)

    return {"chat_history": memoria, "question": state["question"], "response": resposta.content}

# Adicionando estados ao LangGraph
workflow.add_node("responder", processar_pergunta)
workflow.set_entry_point("responder")
workflow.add_edge("responder", END)

# Compilando o Grafo do Agente
agente = workflow.compile()

def iniciar_chat():
    """Inicia o chat interativo com memória persistente"""
    print("✅ Agente Inteligente com LangGraph iniciado! (Versão Corrigida)")
    print("Digite 'sair' para encerrar ou 'limpar' para resetar a memória.\n")

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando o agente...")
            break
        elif pergunta.lower() in ["limpar", "resetar"]:
            memoria.clear()
            print("🧠 Memória apagada! O agente esqueceu a conversa anterior.")
            continue

        resposta = agente.invoke({"chat_history": memoria, "question": pergunta})

        if "response" in resposta:
            print("Agente:", resposta["response"])
        else:
            print("⚠️ Erro: A resposta não foi gerada corretamente.")

# Executa o agente no terminal
if __name__ == "__main__":
    iniciar_chat()
