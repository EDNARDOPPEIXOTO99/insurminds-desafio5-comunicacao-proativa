"""
Agente 2 — Identificação de eventos climáticos relevantes.

Recebe os dados brutos coletados pelo Agente 1 (ColetorClimaticoAgent) e
aplica limiares para decidir se há um evento relevante o suficiente para
gerar um alerta preventivo.

Limiares (configuráveis via variáveis de ambiente, ver .env.example):
- Chuva intensa: volume de chuva na última 1h acima de LIMIAR_CHUVA_MM
- Vento forte: velocidade do vento acima de LIMIAR_VENTO_MS
- Tempestade / risco de granizo: condição meteorológica no grupo
  "Thunderstorm" da OpenWeatherMap (códigos 200-232), usada aqui como
  proxy de risco de granizo, já que o plano gratuito da API não informa
  ocorrência de granizo diretamente.
"""

import os

LIMIAR_CHUVA_MM = float(os.getenv("LIMIAR_CHUVA_MM", "10"))
LIMIAR_VENTO_MS = float(os.getenv("LIMIAR_VENTO_MS", "12"))
FAIXA_TEMPESTADE = range(200, 233)  # códigos "Thunderstorm" da OpenWeatherMap


class AnalisadorEventosAgent:
    """Agente responsável por transformar dados climáticos brutos em uma
    lista de eventos relevantes (ou nenhum, se as condições forem normais)."""

    def analisar(self, dados_clima: dict) -> list[dict]:
        if dados_clima.get("erro"):
            return []

        eventos = []
        cidade = dados_clima["cidade"]
        uf = dados_clima["uf"]

        chuva = dados_clima.get("chuva_mm_1h") or 0.0
        if chuva >= LIMIAR_CHUVA_MM:
            eventos.append({
                "cidade": cidade,
                "uf": uf,
                "tipo": "chuva_intensa",
                "descricao": f"Chuva intensa detectada ({chuva:.1f} mm/h)",
                "severidade": "alta" if chuva >= LIMIAR_CHUVA_MM * 2 else "moderada",
            })

        vento = dados_clima.get("vento_velocidade_ms") or 0.0
        if vento >= LIMIAR_VENTO_MS:
            eventos.append({
                "cidade": cidade,
                "uf": uf,
                "tipo": "vento_forte",
                "descricao": f"Ventos fortes detectados ({vento:.1f} m/s)",
                "severidade": "alta" if vento >= LIMIAR_VENTO_MS * 1.5 else "moderada",
            })

        condicao_id = dados_clima.get("condicao_id")
        if condicao_id in FAIXA_TEMPESTADE:
            eventos.append({
                "cidade": cidade,
                "uf": uf,
                "tipo": "tempestade",
                "descricao": f"Tempestade detectada ({dados_clima.get('condicao_descricao')}) "
                              f"— risco de granizo",
                "severidade": "alta",
            })

        return eventos

    def analisar_varias(self, lista_dados_clima: list[dict]) -> list[dict]:
        eventos = []
        for dados in lista_dados_clima:
            eventos.extend(self.analisar(dados))
        return eventos
