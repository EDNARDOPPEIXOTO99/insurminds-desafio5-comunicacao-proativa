"""
InsurMinds - Desafio 5
Ferramenta Inteligente para Comunicação Proativa com o Segurado

Execução:
    streamlit run app.py
"""

import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.event_agent import AnalisadorEventosAgent
from src.message_agent import GeradorMensagemAgent
from src.notify_agent import SimuladorEnvioAgent
from src.rules_agent import RegrasNegocioAgent
from src.weather_agent import ColetorClimaticoAgent

load_dotenv()

st.set_page_config(page_title="InsurMinds - Desafio 5", page_icon="🌩️", layout="wide")
st.title("🌩️ Comunicação Proativa com o Segurado")
st.caption("Desafio 5 · InsurMinds · I2A2 — Grupo InsurTech Minds")

SEGURADOS_PATH = os.path.join("data", "segurados.csv")


@st.cache_data
def carregar_segurados():
    return pd.read_csv(SEGURADOS_PATH)


segurados_df = carregar_segurados()

with st.sidebar:
    st.header("Base de segurados (fictícia)")
    st.dataframe(segurados_df, use_container_width=True, hide_index=True)
    st.caption(f"{len(segurados_df)} segurados em {segurados_df['cidade'].nunique()} cidades.")
    st.divider()
    provider = os.getenv("LLM_PROVIDER", "google")
    st.caption(f"Provedor de IA: **{provider}** (configurável no `.env`)")

st.header("Executar o fluxo completo")
st.write(
    "Ao clicar no botão abaixo, o sistema: (1) consulta o clima atual de cada "
    "cidade via OpenWeatherMap, (2) identifica eventos relevantes, (3) aplica "
    "as regras de negócio para saber quem deve ser notificado, (4) gera uma "
    "mensagem personalizada por IA para cada segurado afetado, e (5) simula "
    "o envio das notificações."
)

if st.button("▶ Buscar clima e gerar alertas", type="primary"):
    try:
        coletor = ColetorClimaticoAgent()
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    analisador = AnalisadorEventosAgent()
    regras = RegrasNegocioAgent(segurados_df)
    gerador = GeradorMensagemAgent()
    simulador = SimuladorEnvioAgent()

    cidades_uf = list(segurados_df[["cidade", "uf"]].itertuples(index=False, name=None))

    with st.spinner("1) Consultando dados climáticos (OpenWeatherMap)..."):
        dados_clima = coletor.coletar_varias_cidades(cidades_uf)

    st.subheader("1) Dados climáticos coletados")
    st.dataframe(pd.DataFrame(dados_clima), use_container_width=True, hide_index=True)

    with st.spinner("2) Identificando eventos relevantes..."):
        eventos = analisador.analisar_varias(dados_clima)

    st.subheader("2) Eventos climáticos relevantes identificados")
    if eventos:
        st.dataframe(pd.DataFrame(eventos), use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum evento relevante detectado nas cidades monitoradas no momento.")

    with st.spinner("3) Aplicando regras de negócio..."):
        notificacoes = regras.aplicar(eventos)

    st.subheader(f"3) Segurados a notificar ({len(notificacoes)})")

    if not notificacoes:
        st.info("Nenhum segurado precisa ser notificado no momento.")
    else:
        st.subheader("4) e 5) Mensagens geradas e envio simulado")
        progress = st.progress(0.0)
        for i, notificacao in enumerate(notificacoes, start=1):
            with st.spinner(f"Gerando mensagem para {notificacao['segurado']['nome']}..."):
                mensagem = gerador.gerar(notificacao)
                registro = simulador.enviar(notificacao, mensagem)

            with st.chat_message("assistant"):
                st.markdown(
                    f"**Para:** {registro['nome']} ({registro['cidade']}) · "
                    f"**Canal:** {registro['canal']} · **Evento:** {registro['tipo_evento']}"
                )
                st.write(mensagem)
                st.caption(f"Status: {registro['status']} — {registro['timestamp']}")

            progress.progress(i / len(notificacoes))

        st.success(f"{len(notificacoes)} notificação(ões) simulada(s) com sucesso.")
