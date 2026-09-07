"""
Agente 1 — Coleta de dados meteorológicos.

Consulta a API pública do OpenWeatherMap (Current Weather Data) para cada
cidade presente na base de segurados e devolve os dados brutos (condição
do tempo, chuva, vento) que o Agente 2 vai analisar.

Documentação da API: https://openweathermap.org/current
"""

import os

import requests

OWM_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class ColetorClimaticoAgent:
    """Agente responsável por buscar dados meteorológicos atuais por cidade."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENWEATHER_API_KEY não configurada. Defina no .env "
                "(veja .env.example) — chave gratuita em https://openweathermap.org/api"
            )

    def coletar(self, cidade: str, uf: str, pais: str = "BR") -> dict:
        """Consulta o clima atual de uma cidade. Retorna um dicionário
        normalizado com os campos relevantes para a análise de eventos."""
        params = {
            "q": f"{cidade},{pais}",
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt_br",
        }
        try:
            resp = requests.get(OWM_BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as exc:
            return {
                "cidade": cidade,
                "uf": uf,
                "erro": str(exc),
            }

        weather = data.get("weather", [{}])[0]
        return {
            "cidade": cidade,
            "uf": uf,
            "condicao_id": weather.get("id"),
            "condicao_principal": weather.get("main"),
            "condicao_descricao": weather.get("description"),
            "temperatura": data.get("main", {}).get("temp"),
            "vento_velocidade_ms": data.get("wind", {}).get("speed"),
            "chuva_mm_1h": data.get("rain", {}).get("1h", 0.0),
            "chuva_mm_3h": data.get("rain", {}).get("3h", 0.0),
        }

    def coletar_varias_cidades(self, cidades_uf: list[tuple[str, str]]) -> list[dict]:
        """Coleta o clima para uma lista de (cidade, uf), evitando repetir
        chamadas para a mesma cidade."""
        vistos = set()
        resultados = []
        for cidade, uf in cidades_uf:
            chave = (cidade, uf)
            if chave in vistos:
                continue
            vistos.add(chave)
            resultados.append(self.coletar(cidade, uf))
        return resultados
