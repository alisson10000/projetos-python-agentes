import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict

# Ajustando o caminho para garantir que o Python encontre database.db_handler
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_handler import salvar_memoria, recuperar_memoria  # Importando o banco de dados

# 🔹 Carregar variáveis do ambiente (.env)
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Verificação da chave da API
if not OPENAI_API_KEY:
    print("⚠️ Erro: A API Key da OpenAI não foi encontrada! Verifique o arquivo .env.")
    exit(1)

# 🔹 Criando o Modelo de IA com LangChain
modelo = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

# 🔹 Criando a Memória Persistente com SQLite
memoria = ChatMessageHistory()

# 🔹 Criando o Prompt do Agente
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Você é um assistente útil e memoriza conversas anteriores."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{question}")
])

# 🔹 Definição do Estado do Agente para LangGraph
class AgentState(TypedDict):
    chat_history: ChatMessageHistory
    question: str
    response: str

# 🔹 Criando o Grafo do Agente (LangGraph)
workflow = StateGraph(AgentState)

# 🔹 Função de Processamento do Agente
def processar_pergunta(state: AgentState) -> Dict:
    """Processa a pergunta do usuário, mantém a memória persistente e interage com a IA."""
    
    pergunta_usuario = state["question"]
    
    # 🔹 Obtém histórico armazenado no banco de dados SQLite
    historico_salvo = recuperar_memoria()
    
    # 🔹 Adiciona a conversa atual ao histórico
    mensagens = historico_salvo + [HumanMessage(content=pergunta_usuario)]

    # 🔹 Gera resposta da IA
    resposta = modelo.invoke(mensagens)

    # 🔹 Armazena na memória persistente
    salvar_memoria(pergunta_usuario, resposta.content)

    return {"chat_history": memoria, "question": pergunta_usuario, "response": resposta.content}

# 🔹 Adicionando estados ao LangGraph
workflow.add_node("responder", processar_pergunta)
workflow.set_entry_point("responder")
workflow.add_edge("responder", END)

# 🔹 Compilando o Grafo do Agente
agente = workflow.compile()

def iniciar_chat():
    """Inicia o chat interativo com memória persistente no SQLite."""
    print("✅ Agente Inteligente com Memória iniciado! (LangChain + SQLite)")
    print("Digite 'sair' para encerrar ou 'limpar' para resetar a memória.\n")

    while True:
        pergunta = input("Você: ")

        if pergunta.lower() in ["sair", "exit", "fechar"]:
            print("Encerrando o agente...")
            break
        
        elif pergunta.lower() in ["limpar", "resetar"]:
            salvar_memoria("Memória resetada", "Histórico apagado")  # Mantém um registro do reset
            print("🧠 Memória apagada! O agente esqueceu a conversa anterior.")
            continue

        resposta = agente.invoke({"chat_history": memoria, "question": pergunta})

        if "response" in resposta:
            print("Agente:", resposta["response"])
        else:
            print("⚠️ Erro: A resposta não foi gerada corretamente.")

# 🔹 Executa o agente no terminal
if __name__ == "__main__":
    iniciar_chat()
