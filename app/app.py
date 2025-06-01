import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import os

# Carregar .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Agora pode importar diretamente
from myagent.crew import MyAgent
from langchain_core.messages import HumanMessage, AIMessage


# ========== INTERFACE ==========
st.set_page_config(page_title="Chat com o Crew", layout="centered")
st.title("🧠 Chat com o Agente (CrewAI)")

# Histórico de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Exibir histórico
for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "ai"
    with st.chat_message(role):
        st.markdown(msg.content)

# Campo de input
user_input = st.chat_input("Digite sua pergunta...")

# Lógica de envio
if user_input:
    # Mostra e armazena mensagem do usuário
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # Chama o Crew e responde
    with st.chat_message("ai"):
        with st.spinner("Pensando com o Crew..."):
            try:

                resposta = MyAgent().crew().kickoff(inputs={"topic": user_input})
                resposta_texto = resposta.content if hasattr(resposta, "content") else str(resposta)
                st.markdown(resposta_texto)
                st.session_state.chat_history.append(AIMessage(content=resposta_texto))
            except Exception as e:
                st.error(f"Erro ao rodar o Crew: {e}")

# Botão para limpar conversa
if st.sidebar.button("🧹 Limpar conversa"):
    st.session_state.chat_history = []
    st.rerun()
