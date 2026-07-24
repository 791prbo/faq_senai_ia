import streamlit as st

# Configuração da página web
st.set_page_config(page_title="FAQ Bot do SENAI", page_icon="🤖")
st.title("🤖 Chatbot FAQ - Versão Web")
st.write("Pergunte sobre horários, cursos ou contato.")

# Banco de dados fixo (Cérebro antigo)
faq = {
    "horário": "Estamos abertos das 8h às 18h.",
    "curso": "Oferecemos cursos de programação e IA de ponta!",
    "contato": "Nosso telefone de contato é (14) 1234-5678."
}

# Inicializando o histórico de mensagens na memória da página (Session State)
if "historico" not in st.session_state:
    st.session_state.historico = []

# Exibir as mensagens anteriores que já estão salvas no histórico
for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# Capturando a entrada do usuário através da caixa de chat do Streamlit
if pergunta_usuario := st.chat_input("Digite sua dúvida aqui..."):
    
    # 1. Mostrar a pergunta do usuário na tela
    with st.chat_message("user"):
        st.markdown(pergunta_usuario)
    
    # Salvar a pergunta no histórico da memória
    st.session_state.historico.append({"role": "user", "content": pergunta_usuario})

    # 2. Processar a resposta usando a lógica antiga de dicionário
    termo_busca = pergunta_usuario.lower()
    
    # Busca simplificada por palavra-chave
    resposta_bot = "Desculpe, ainda sou um robô limitado. Não entendi sua pergunta."
    for chave in faq:
        if chave in termo_busca:
            resposta_bot = faq[chave]
            break

    # 3. Mostrar a resposta do robô na tela
    with st.chat_message("assistant"):
        st.markdown(resposta_bot)
        
    # Salvar a resposta no histórico da memória
    st.session_state.historico.append({"role": "assistant", "content": resposta_bot})