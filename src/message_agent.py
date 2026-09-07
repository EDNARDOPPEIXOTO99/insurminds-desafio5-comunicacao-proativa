"""
Agente 4 — Geração de mensagens personalizadas com IA Generativa.

Recebe uma notificação (segurado + evento climático) montada pelo Agente 3
e usa um LLM para redigir uma mensagem curta, natural e preventiva, no
tom de uma seguradora se comunicando proativamente com o cliente.

Suporta os mesmos provedores usados no Desafio 4 (Google Gemini,
Anthropic, OpenAI, Ollama), configuráveis via LLM_PROVIDER no .env.
"""

import os


def _get_llm():
    provider = os.getenv("LLM_PROVIDER", "google").lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.4)

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"), temperature=0.4)

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.1"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.4,
        )

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(
        model=os.getenv("GOOGLE_MODEL", "gemini-flash-lite-latest"),
        temperature=0.4,
    )


PROMPT_TEMPLATE = """Você é o time de comunicação de uma seguradora, escrevendo um alerta
preventivo curto para um segurado, em português do Brasil.

Dados do segurado:
- Nome: {nome}
- Cidade/UF: {cidade}/{uf}
- Tipo de seguro: {tipo_seguro}
- Canal de envio: {canal}

Evento climático detectado:
- Tipo: {tipo_evento}
- Descrição: {descricao_evento}
- Severidade: {severidade}

Escreva uma mensagem curta (máximo 3-4 frases), personalizada com o nome do
segurado, explicando o risco de forma clara e oferecendo 1 ou 2 recomendações
preventivas concretas relacionadas ao tipo de seguro dele. Tom profissional,
mas acolhedor — sem alarmismo. Não invente números ou promessas de cobertura.
Escreva apenas a mensagem final, sem comentários adicionais.
"""


class GeradorMensagemAgent:
    """Agente responsável por gerar, via LLM, a mensagem final para cada
    notificação (segurado + evento)."""

    def __init__(self):
        self.llm = _get_llm()

    def gerar(self, notificacao: dict) -> str:
        segurado = notificacao["segurado"]
        evento = notificacao["evento"]

        prompt = PROMPT_TEMPLATE.format(
            nome=segurado["nome"],
            cidade=segurado["cidade"],
            uf=segurado["uf"],
            tipo_seguro=segurado["tipo_seguro"],
            canal=segurado["canal_contato"],
            tipo_evento=evento["tipo"].replace("_", " "),
            descricao_evento=evento["descricao"],
            severidade=evento["severidade"],
        )

        response = self.llm.invoke(prompt)
        return _extract_text(response.content)


def _extract_text(content) -> str:
    """Normaliza a resposta do LLM para string (alguns modelos, como o
    Gemini, retornam uma lista de blocos em vez de uma string simples)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text"]
        if parts:
            return "\n".join(parts)
    return str(content)
