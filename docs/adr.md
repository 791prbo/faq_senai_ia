# ADR 001: Escolha da Arquitetura do Chatbot SENAI

## Status
Aprovado.

## Contexto
Necessidade de criar uma aplicação didática e funcional de Inteligência Artificial para treinamento de alunos, com injeção dinâmica de contexto (documentos institucionais) sem alto custo de infraestrutura.

## Decisões Tomadas
1. **Framework Web: Streamlit**
   - *Motivo:* Permite criar interfaces reativas e modernas em 100% Python, eliminando a necessidade de ensinar HTML/CSS/JS no mesmo módulo.
2. **Armazenamento em Memória (`st.session_state`) vs Banco de Dados**
   - *Motivo:* Elimina a complexidade de configurar SGBD (PostgreSQL/MongoDB) para um protótipo, focando o aprendizado no ecossistema de LLMs.
3. **Roteamento nativo via `st.Page`**
   - *Motivo:* Garante isolamento de papéis (Usuário vs Admin) mantendo nomes de arquivos limpos e sem dependência de caracteres especiais no terminal/Git.
4. **Provedores Duplos de IA (G4F e Groq)**
   - *Motivo:* Garante alta disponibilidade (fallback caso um serviço falhe) e permite ao aluno comparar latência, limites de taxa e qualidade de resposta entre modelos (GPT-4o vs Llama 3.3).