# InsurMinds — Desafio 5
## Ferramenta Inteligente para Comunicação Proativa com o Segurado

**Grupo InsurTech Minds**

Protótipo (MVP) que monitora condições meteorológicas em tempo real e gera
comunicações automáticas e personalizadas para segurados, antes que um
sinistro ocorra — transformando o modelo reativo das seguradoras em uma
abordagem preventiva.

## Arquitetura (multiagente)

```
1) ColetorClimaticoAgent  → consulta a API OpenWeatherMap por cidade
2) AnalisadorEventosAgent → identifica eventos relevantes (chuva/vento/tempestade)
3) RegrasNegocioAgent     → decide quais segurados devem ser notificados
4) GeradorMensagemAgent   → gera a mensagem personalizada via LLM (Gemini)
5) SimuladorEnvioAgent    → registra o envio simulado (sem integração real)
```

Cada agente é um módulo independente em `src/`, orquestrado pelo `app.py`
(Streamlit), que exibe o resultado de cada etapa na tela.

## Tecnologias

- Python 3.10+
- Streamlit (interface)
- requests (consumo da API OpenWeatherMap)
- LangChain + Google Gemini (gratuito) para geração das mensagens —
  também suporta Ollama (local/gratuito), Claude e GPT (pagos)
- pandas (base de segurados)

## Fonte de dados meteorológicos

**OpenWeatherMap** (Current Weather Data API) — https://openweathermap.org/api
Camada gratuita, cadastro sem cartão de crédito.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuração

```bash
cp .env.example .env
```

Preencha no `.env`:
1. `OPENWEATHER_API_KEY` — gere gratuitamente em https://openweathermap.org/api
2. `LLM_PROVIDER=google` + `GOOGLE_API_KEY` — gere gratuitamente em https://aistudio.google.com/apikey

> Não é obrigatório pagar por nenhuma API. Ambas as chaves acima têm
> camada gratuita sem necessidade de cartão.

## Execução

```bash
streamlit run app.py
```

Clique em **"Buscar clima e gerar alertas"**. A aplicação vai:
1. Consultar o clima atual de cada cidade da base de segurados
2. Identificar eventos relevantes (chuva intensa, vento forte, tempestade/risco de granizo)
3. Aplicar as regras de negócio (evento → tipo de seguro afetado)
4. Gerar uma mensagem personalizada por IA para cada segurado impactado
5. Simular o envio e exibir o resultado na tela

> Como os dados climáticos são consultados **em tempo real**, os eventos
> disparados dependem do clima do dia em que você rodar a aplicação. Se
> nenhuma das 10 cidades da base estiver com chuva/vento forte no momento,
> nenhuma notificação será gerada — isso é o comportamento correto do
> sistema, não um bug. Para testar a geração de mensagens a qualquer
> momento, ajuste temporariamente os limiares no `.env`
> (`LIMIAR_CHUVA_MM`, `LIMIAR_VENTO_MS`) para valores bem baixos.

## Regras de negócio implementadas

| Evento detectado | Tipo(s) de seguro notificado(s) |
|---|---|
| Chuva intensa | Residencial |
| Tempestade (risco de granizo) | Automóvel e Residencial |
| Vento forte | Residencial |

## Estrutura do projeto

```
insurminds_desafio5/
├── app.py                   # Orquestração dos 5 agentes (Streamlit)
├── src/
│   ├── weather_agent.py     # Agente 1 — coleta de dados climáticos
│   ├── event_agent.py       # Agente 2 — identificação de eventos
│   ├── rules_agent.py       # Agente 3 — regras de negócio
│   ├── message_agent.py     # Agente 4 — geração de mensagens (LLM)
│   └── notify_agent.py      # Agente 5 — simulação de envio
├── data/
│   └── segurados.csv        # Base fictícia de segurados
├── requirements.txt
├── .env.example
└── README.md
```

## Observações

- A base de segurados (`data/segurados.csv`) é fictícia, criada para fins
  didáticos, cobrindo 10 cidades brasileiras (incluindo regiões costeiras)
  e 2 tipos de seguro (Residencial e Automóvel), com 20 segurados no total.
- Não há envio real de SMS/e-mail — apenas simulação, conforme os
  requisitos do desafio.
- Chaves de API nunca devem ser commitadas — ficam apenas no `.env`
  (no `.gitignore`).

## Licença

MIT

## Integrantes do grupo — InsurTech Minds

| Nome | Papel |
|---|---|
| Ednardo Pinheiro Peixoto | Representante e Engenheiro de IA/IoT/Tech Líder |
| Glenda dos Santos Tavares | Atuária |
| Sueli Da Hora Moreira | Analytics Engineer |
| Rafael Torres Lattaro Soares | Especialista em Seguros |
