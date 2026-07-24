import tiktoken
import streamlit as st
from g4f.client import Client # Importando o cliente unificado de IA

def calcular_tokens_oficial(texto, modelo="gpt-4o-mini"):
    try:
        # Puxa o codificador oficial da OpenAI configurado para aquele modelo
        codificador = tiktoken.encoding_for_model(modelo)
    except KeyError:
        # Caso o modelo seja genérico, usa o padrão do GPT-4
        codificador = tiktoken.get_encoding("cl100k_base")
        
    # O método .encode() transforma o texto puro em uma lista de números (IDs dos tokens)
    lista_de_tokens = codificador.encode(texto)
    
    # Retornamos o tamanho dessa lista (que é a quantidade exata de tokens)
    return len(lista_de_tokens)

# Configuração da página web
st.set_page_config(page_title="AI Chatbot Pro", page_icon="🧠")
st.title("🧠 Meu Chatbot com IA Generativa")
st.write("Conectado diretamente a modelos de linguagem avançados. Pergunte o que quiser!")

# Inicializando o cliente da API (O nosso 'garçom' de requisições)
client = Client()

# Inicializando o histórico de mensagens na memória da sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        # Mensagem de sistema que dita o comportamento inicial da IA
        {"role": "system", "content": "Você é um assistente virtual prestativo e bem-humorado criado em sala de aula."}
    ]
# ==============================================================================
# 📊 BARRA LATERAL: Monitor de Consumo de Tokens (A Novidade aqui)
# ==============================================================================
with st.sidebar:
    st.header("📊 Monitor de Infraestrutura")
    st.write("Tamanho do 'cérebro' enviado para a API nesta rodada:")
    
    # Calcular o total de tokens atualmente acumulados no histórico
    total_tokens_prompt = sum(calcular_tokens_oficial(msg["content"]) for msg in st.session_state.mensagens)
    
    # Exibe um card visual elegante com a métrica
    st.metric(
        label="Tokens de Entrada (Contexto Atual)", 
        value=f"{total_tokens_prompt} tokens",
        delta=f"+{calcular_tokens_oficial(st.session_state.mensagens[-1]['content'])} do último turno" if len(st.session_state.mensagens) > 1 else None
    )
    
    st.divider()
    st.caption("⚠️ Nota técnica: Como o histórico é reenviado a cada mensagem, o custo de processamento cresce de forma cumulativa.")        

# Renderizar as mensagens anteriores na tela (ignorando a mensagem oculta do 'system')
for msg in st.session_state.mensagens:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Caixa de entrada de texto para o usuário interagir
if prompt := st.chat_input("Envie uma mensagem para a IA..."):
    
    # 1. Exibir e salvar a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.mensagens.append({"role": "user", "content": prompt})

    # 2. Chamar a API externa para processar a resposta de forma inteligente
    with st.chat_message("assistant"):
        # Criando um elemento de carregamento visual (spinner) enquanto a internet responde
        with st.spinner("Pensando..."):
            try:
                # Requisição oficial de chat completions
                resposta_api = client.chat.completions.create(
                    model="gpt-4o-mini", # Especificando o modelo cognitivo desejado
                    messages=st.session_state.mensagens # Enviando TODO o histórico para dar contexto
                )
                
                # Extraindo o texto puro de dentro do payload retornado pela API
                texto_resposta = resposta_api.choices[0].message.content
                
                # Exibindo o resultado final processado pela IA na tela do usuário
                st.markdown(texto_resposta)
                
                # 3. Salvar a resposta gerada no histórico para manter o contexto na próxima pergunta
                st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})
                
            except Exception as e:
                # Tratamento de erro caso o provedor da API gratuita falhe temporariamente
                st.error("Ops! Tive um problema para conectar ao servidor de IA.")
                st.caption(f"Detalhe técnico do erro: {e}")