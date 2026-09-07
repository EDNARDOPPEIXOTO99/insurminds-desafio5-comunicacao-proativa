"""
Agente 5 — Simulação de envio das notificações.

O edital do desafio explicitamente NÃO pede envio real de SMS/e-mail —
apenas a simulação do processo. Este agente registra cada notificação
"enviada" (nome, canal, evento, mensagem, horário) para exibição na
interface e para o relatório, sem nenhuma integração externa real.
"""

from datetime import datetime


class SimuladorEnvioAgent:
    """Agente responsável por simular o envio de uma notificação."""

    def __init__(self):
        self.historico: list[dict] = []

    def enviar(self, notificacao: dict, mensagem: str) -> dict:
        segurado = notificacao["segurado"]
        evento = notificacao["evento"]

        registro = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": segurado["nome"],
            "cidade": f'{segurado["cidade"]}/{segurado["uf"]}',
            "canal": segurado["canal_contato"],
            "tipo_evento": evento["tipo"],
            "mensagem": mensagem,
            "status": "simulado (nenhum envio real foi realizado)",
        }
        self.historico.append(registro)
        return registro
