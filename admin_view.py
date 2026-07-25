# Visão 2: Painel Administrativo
import streamlit as st
from services import extrair_texto_de_arquivo, gerar_template_word_bytes
from config import TEMPLATE_TXT

st.title("⚙️ Painel de Administração - Base de Conhecimento")

st.markdown("""
Esta área é destinada à coordenação do SENAI para gestão dos documentos e editais oficiais.
""")

st.divider()

# --- SEÇÃO DE DOWNLOAD DE TEMPLATES ---
st.subheader("📋 Baixar Modelos de Template")
st.write("Baixe o modelo preenchível abaixo para cadastrar novos cursos no formato correto:")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="📄 Baixar Modelo (.txt)",
        data=TEMPLATE_TXT,  # 👈 Usando a variável importada do config.py
        file_name="template_cursos_senai.txt",
        mime="text/plain",
        use_container_width=True
    )

with col2:
    buffer_docx = gerar_template_word_bytes()
    st.download_button(
        label="📝 Baixar Modelo (.docx)",
        data=buffer_docx,
        file_name="template_cursos_senai.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )

st.divider()

arquivo_enviado = st.file_uploader(
    "Envie o arquivo oficial de cursos (.pdf, .txt ou .docx):",
    type=["txt", "pdf", "docx"]
)

if arquivo_enviado:
    texto_extraido = extrair_texto_de_arquivo(arquivo_enviado)
    st.session_state["base_conhecimento_extra"] = texto_extraido
    
    st.success(f"✅ Arquivo **'{arquivo_enviado.name}'** carregado na memória do sistema!")
    st.info(f"📊 Total de caracteres extraídos: {len(texto_extraido)}")

if "base_conhecimento_extra" in st.session_state:
    st.divider()
    if st.button("🗑️ Remover Base Adicional"):
        del st.session_state["base_conhecimento_extra"]
        st.success("Base adicional removida.")
        st.rerun()