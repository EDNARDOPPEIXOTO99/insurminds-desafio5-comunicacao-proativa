"""
Agente 3 — Regras de negócio.

Decide, para cada evento climático identificado pelo Agente 2, quais
segurados (por cidade + tipo de seguro) devem receber uma notificação
preventiva.

Regras (baseadas nos exemplos citados no próprio edital do desafio):
- chuva_intensa   -> segurados com seguro Residencial
- tempestade       -> segurados com seguro Automóvel (risco de granizo) e Residencial
- vento_forte      -> segurados com seguro Residencial (ênfase em regiões costeiras)
"""

import pandas as pd

REGRAS_EVENTO_TIPO_SEGURO = {
    "chuva_intensa": ["Residencial"],
    "tempestade": ["Automóvel", "Residencial"],
    "vento_forte": ["Residencial"],
}


class RegrasNegocioAgent:
    """Agente responsável por cruzar eventos climáticos com a base de
    segurados, aplicando as regras de negócio do domínio de seguros."""

    def __init__(self, segurados_df: pd.DataFrame):
        self.segurados_df = segurados_df

    def aplicar(self, eventos: list[dict]) -> list[dict]:
        """Retorna uma lista de notificações a gerar, no formato:
        {"segurado": <linha do DataFrame como dict>, "evento": <evento>}"""
        notificacoes = []
        for evento in eventos:
            tipos_seguro_alvo = REGRAS_EVENTO_TIPO_SEGURO.get(evento["tipo"], [])
            if not tipos_seguro_alvo:
                continue

            afetados = self.segurados_df[
                (self.segurados_df["cidade"] == evento["cidade"])
                & (self.segurados_df["uf"] == evento["uf"])
                & (self.segurados_df["tipo_seguro"].isin(tipos_seguro_alvo))
            ]

            for _, segurado in afetados.iterrows():
                notificacoes.append({
                    "segurado": segurado.to_dict(),
                    "evento": evento,
                })

        return notificacoes
