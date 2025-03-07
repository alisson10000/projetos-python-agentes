import os
import mysql.connector
from dotenv import load_dotenv

# 🔹 Carregar variáveis do ambiente (.env)
load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))

# 🔹 Configurações do MariaDB
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 🔹 Conectar ao banco de dados
def conectar():
    """Estabelece conexão com o banco de dados MariaDB."""
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# 🔹 Criar tabela se não existir
def inicializar_banco():
    """Cria a tabela de histórico de conversas, caso não exista."""
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_conversa (
                id INT AUTO_INCREMENT PRIMARY KEY,
                remetente ENUM('user', 'ai'),
                mensagem TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conexao.commit()
        cursor.close()
        conexao.close()

# 🔹 Salvar mensagem no banco
def salvar_mensagem(remetente, mensagem):
    """Armazena mensagens do usuário ou da IA no banco de dados."""
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO historico_conversa (remetente, mensagem) VALUES (%s, %s)", (remetente, mensagem))
        conexao.commit()
        cursor.close()
        conexao.close()

# 🔹 Recuperar histórico de mensagens
def recuperar_historico():
    """Obtém todas as mensagens armazenadas no banco de dados."""
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT remetente, mensagem FROM historico_conversa ORDER BY timestamp ASC")
        mensagens = cursor.fetchall()
        cursor.close()
        conexao.close()

        # Retorna mensagens formatadas para LangChain
        return [{"role": remetente, "content": mensagem} for remetente, mensagem in mensagens]
    return []

# 🔹 Executa a criação da tabela ao importar o módulo
inicializar_banco()
