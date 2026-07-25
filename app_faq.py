import streamlit as st
from config import PROMPT_SISTEMA_SENAI
from services import calcular_tokens, gerar_resposta_ia

# Leitura da chave do arquivo de segredos
GROQ_KEY = st.secrets.get("GROQ_API_KEY", None)

# Configuração da tela
st.set_page_config(page_title="AI Chatbot SENAI", page_icon="🤖", layout="wide")
st.title("🤖 Chatbot Multi-API - SENAI")

# Inicialização do estado da sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "system", "content": PROMPT_SISTEMA_SENAI}
    ]

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Provedor de IA")
    provedor = st.selectbox(
        "Escolha a IA:",
        ["GPT-4o Mini (Via G4F)", "Llama 3.3 70B (Via Groq)"]
    )
    
    st.divider()
    
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.mensagens = [{"role": "system", "content": PROMPT_SISTEMA_SENAI}]
        st.rerun()

    st.divider()
    
    total_tokens = sum(calcular_tokens(m["content"]) for m in st.session_state.mensagens)
    st.metric("Tokens Acumulados", f"{total_tokens} tokens")

# --- INTERFACE DE CHAT ---
for msg in st.session_state.mensagens:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Pergunte sobre os cursos do SENAI..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.mensagens.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner(f"Processando pelo {provedor}..."):
            try:
                # O app.py não sabe COMO a IA responde, só chama o serviço!
                resposta = gerar_resposta_ia(provedor, st.session_state.mensagens, GROQ_KEY)
                st.markdown(resposta)
                st.session_state.mensagens.append({"role": "assistant", "content": resposta})
                st.rerun()
            except Exception as e:
                st.error("Erro na comunicação com o provedor.")
                st.caption(f"Detalhes técnicos: {e}")