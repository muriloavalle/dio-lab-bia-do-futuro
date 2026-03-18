import json
import pandas as pd
import requests
import streamlit as st

#Configuracao
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# Carregar Dados
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

# Montar Contexto
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMONIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSACOES RECENTES :
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONIVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# System Prompt
SYSTEM_PROMPT = """Voce e o Edu, um educador financeiro amigavel e didatico.

OBJETIVO:
Ensinar Conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
- NUNCA recomende investimentos especificos, apenas explique como funcionam;
- JAMAIS responda a perguntas fora do tema ensino de financas pessoais.
    Quando ocorrer, responda lembrando o seu papel de educador financeiro;
- Use os dados fornecidos para dar exemplos personalizados;
- Linguagem simples, como se explicasse para um amigo;
- Se não souber de algo, admita: "Não tenho essa informação, mas posso explicar...";
- Sempre pergunte se o cliente entendeu.
- Responda de forma sucinta e direta, com no maximo 3 paragrafos.
"""

# Chamar Ollama
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# Interface
st.title("🎓 Edu, seu educador financeiro")

if pergunta := st.chat_input("Sua duvida sobre financas..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
