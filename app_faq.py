import streamlit as st
from config import PROMPT_SISTEMA_SENAI
from services import calcular_tokens, gerar_resposta_ia

GROQ_KEY = st.secrets.get("GROQ_API_KEY", None)

st.set_page_config(page_title="AI Chatbot SENAI", page_icon="🤖", layout="wide")
st.title("🤖 Chatbot Multi-API - SENAI")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "system", "content": PROMPT_SISTEMA_SENAI}
    ]

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Provedor & Parâmetros")
    provedor = st.selectbox(
        "Escolha a IA:",
        ["GPT-4o Mini (Via G4F)", "Llama 3.3 70B (Via Groq)"]
    )
    
    # 🎛️ Controle deslizante de Temperatura
    temperatura = st.slider(
        "Criatividade (Temperatura):",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1,
        help="0.0 = Preciso/Técnico | 1.0 = Criativo/Variado"
    )
    
    st.divider()
    
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.mensagens = [{"role": "system", "content": PROMPT_SISTEMA_SENAI}]
        st.rerun()

    st.divider()
    
    total_tokens = sum(calcular_tokens(m["content"]) for m in st.session_state.mensagens)
    st.metric("Tokens Acumulados", f"{total_tokens} tokens")

# --- CHAT ---
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
                # Recebe a resposta E o tempo de execução
                resposta, tempo_execucao = gerar_resposta_ia(provedor, st.session_state.mensagens, GROQ_KEY, temperatura)
                
                # Exibe a resposta
                st.markdown(resposta)
                
                # Exibe a métrica e os botões de feedback
                st.caption(f"⚡ Resposta gerada em **{tempo_execucao}s** (Temperatura: `{temperatura}`)")
                
                col1, col2, _ = st.columns([1, 1, 10])
                with col1:
                    if st.button("👍", key=f"up_{len(st.session_state.mensagens)}"):
                        st.toast("Feedback positivo registrado!")
                with col2:
                    if st.button("👎", key=f"down_{len(st.session_state.mensagens)}"):
                        st.toast("Feedback negativo registrado.")

                st.session_state.mensagens.append({"role": "assistant", "content": resposta})
                st.rerun()
                
            except Exception as e:
                st.error("Erro na comunicação com o provedor.")
                st.caption(f"Detalhes técnicos: {e}")