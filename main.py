# 🚀 ROTEADOR CENTRAL (Entrypoint)
import streamlit as st

# 1. Definição das Páginas (Ícones, Títulos e Scripts)
pagina_chat = st.Page(
    "chat_view.py", 
    title="Consultor SENAI", 
    icon="💬", 
    default=True
)

pagina_admin = st.Page(
    "admin_view.py", 
    title="Painel Admin", 
    icon="⚙️"
)

# 2. Organização do Menu por Seções
pg = st.navigation({
    "Atendimento": [pagina_chat],
    "Gerenciamento": [pagina_admin]
})

# 3. Execução da Rota Selecionada
pg.run()