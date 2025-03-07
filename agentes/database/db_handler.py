import sqlite3
import os

# Definir o caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# 🔹 Criando a tabela do banco de dados
def inicializar_db():
    """Cria a tabela para armazenar mensagens se ela não existir."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT,
                agente TEXT
            )
        """)
        conn.commit()

# 🔹 Função para salvar uma nova interação no banco
def salvar_memoria(usuario, agente):
    """Salva a conversa entre o usuário e o agente no banco SQLite."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO memoria (usuario, agente) VALUES (?, ?)", (usuario, agente))
        conn.commit()

# 🔹 Função para recuperar o histórico de conversas
def recuperar_memoria():
    """Recupera todas as conversas armazenadas no banco de dados."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, agente FROM memoria")
        resultados = cursor.fetchall()

    # Convertendo para o formato esperado por LangChain
    historico = []
    for usuario, agente in resultados:
        historico.append({"role": "user", "content": usuario})
        historico.append({"role": "assistant", "content": agente})
    
    return historico

# 🔹 Inicializa o banco ao importar o módulo
inicializar_db()
