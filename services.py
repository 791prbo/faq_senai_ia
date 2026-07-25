# Camada 2: Lógica de IA & Processamento
import time
import tiktoken
from g4f.client import Client
from groq import Groq
from config import MODELO_DEFAULT_G4F, MODELO_DEFAULT_GROQ

def calcular_tokens(texto, modelo="gpt-4o-mini"):
    try:
        codificador = tiktoken.encoding_for_model(modelo)
    except KeyError:
        codificador = tiktoken.get_encoding("cl100k_base")
    return len(codificador.encode(texto))

def gerar_resposta_ia(provedor, mensagens, groq_key=None, temperatura=0.2):
    inicio = time.time()  # ⏱️ Inicia a contagem de tempo
    
    if provedor == "GPT-4o Mini (Via G4F)":
        client = Client()
        resposta = client.chat.completions.create(
            model=MODELO_DEFAULT_G4F,
            messages=mensagens,
            temperature=temperatura  # 🎛️ Parâmetro de temperatura
        )
        texto = resposta.choices[0].message.content

    elif provedor == "Llama 3.3 70B (Via Groq)":
        if not groq_key:
            raise ValueError("Chave 'GROQ_API_KEY' não foi encontrada no secrets.toml.")
        
        client_groq = Groq(api_key=groq_key)
        resposta = client_groq.chat.completions.create(
            model=MODELO_DEFAULT_GROQ,
            messages=mensagens,
            temperature=temperatura  # 🎛️ Parâmetro de temperatura
        )
        texto = resposta.choices[0].message.content
    else:
        raise ValueError("Provedor de IA desconhecido.")

    tempo_decorrido = round(time.time() - inicio, 2)  # 📊 Calcula os segundos
    return texto, tempo_decorrido