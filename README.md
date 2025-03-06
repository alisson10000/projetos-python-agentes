# projetos-python-agentes

Estudo para criação de agentes de IA em Python utilizando OpenAI, LangChain e LangGraph.
O projeto inclui memória persistente, chamadas de API externas e versionamento via Gitea.

# 🚀 Projetos Python - Agentes Inteligentes 🤖

Este repositório contém estudos e implementações de **Agentes de Inteligência Artificial em Python**, 
utilizando LangChain, LangGraph, OpenAI e APIs externas.

## 📌 Tecnologias Utilizadas:
- Python 3.12
- LangChain & LangGraph
- OpenAI API
- Gitea para versionamento

## 📂 Estrutura do Projeto:
📂 `agentes/` → Código dos agentes de IA  
📂 `config/` → Configurações e chaves de API  
📂 `build/` → Arquivos gerados pelo PyInstaller  
📂 `logs/` → Logs e depuração  

##📌 ⚡ Como Usar: Instalação e Execução do Agente de IA
1️⃣ Clonar o Repositório
Abra o terminal (cmd, PowerShell ou Git Bash) e execute:

git clone http://server1.setorzero.com:1977/alisson/projetos-python-agentes.git
cd projetos-python-agentes
2️⃣ Criar e Ativar o Ambiente Virtual
🔹 Para evitar conflitos entre versões de pacotes, usamos um ambiente virtual.

✅ No Windows (PowerShell)

python -m venv venv
venv\Scripts\activate
✅ No Linux/macOS (Terminal)

python3 -m venv venv
source venv/bin/activate
3️⃣ Instalar as Dependências
Agora, instale todas as bibliotecas necessárias:

pip install -r requirements.txt
📌 Se o arquivo requirements.txt não existir, execute:

pip install openai langchain langchain_community langchain_core langchain_text_splitters langchain_openai langgraph google-generativeai python-dotenv requests
pip freeze > requirements.txt  # Salva as dependências no arquivo
4️⃣ Configurar as Chaves de API
Antes de rodar o agente, precisamos configurar as chaves API.

	1️⃣ Abra o arquivo .env dentro da pasta config/ e adicione:

	OPENAI_API_KEY= "SUA_CHAVE_OPENAI"
	GEMINI_API_KEY= "SUA_CHAVE_GEMINI"
	GNEWS_API_KEY= "SUA_CHAVE_GNEWS"
	2️⃣ Se não tiver o arquivo .env, crie-o com:

	echo OPENAI_API_KEY="SUA_CHAVE_OPENAI" > config/.env
	echo GEMINI_API_KEY="SUA_CHAVE_GEMINI" >> config/.env
	echo GNEWS_API_KEY="SUA_CHAVE_GNEWS" >> config/.env
5️⃣ Executar o Agente de IA
Agora podemos rodar o agente!

python agentes/agente_langchain.py
Se quiser testar outros agentes:

python agentes/agente_clima.py
python agentes/agente_memoria.py

6️⃣ Atualizar o Código
Se precisar atualizar o projeto com as últimas mudanças do Gitea:

git pull origin main
📌 🚀 Conclusão
✅ Agora qualquer pessoa pode clonar, instalar e rodar o agente sem problemas!
✅ Com as bibliotecas organizadas, fica fácil manter tudo atualizado.

🔥 Se precisar adicionar mais alguma coisa, só avisar! 🚀💡new