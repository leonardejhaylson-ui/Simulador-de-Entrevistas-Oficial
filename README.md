# Simulador de Entrevistas Técnicas

Bot experimental para Telegram que utiliza um modelo de linguagem para gerar perguntas e fornecer feedback em entrevistas técnicas de nível júnior.

O projeto foi criado para praticar integração de APIs, programação assíncrona em Python, persistência com SQLite e uso de LLMs em um fluxo conversacional.

## Funcionalidades atuais

- comando `/start` com instruções;
- início de entrevista por tecnologia com `/entrevista`;
- suporte a Python, Java, SQL, JavaScript e C;
- geração da primeira pergunta pelo Gemini;
- avaliação da resposta do usuário e geração da pergunta seguinte;
- controle do estado da entrevista em SQLite;
- registro local das mensagens da sessão;
- encerramento e limpeza da sessão com `/parar`;
- credenciais carregadas por variáveis de ambiente.

## Tecnologias

- Python 3
- python-telegram-bot
- Google Gen AI SDK
- Gemini 2.5 Flash
- SQLite
- python-dotenv

## Fluxo

```text
Telegram
   ↓
Bot Python
   ├── SQLite (estado e mensagens)
   └── Gemini API (perguntas e feedback)
```

> O histórico é persistido localmente, mas a implementação atual não reconstrói todo o histórico da conversa no contexto enviado ao modelo. Este repositório deve ser tratado como protótipo de aprendizado, não como plataforma de avaliação técnica validada.

## Configuração

```bash
git clone https://github.com/leonardejhaylson-ui/Simulador-de-Entrevistas-Oficial.git
cd Simulador-de-Entrevistas-Oficial

python -m venv .venv
```

Ative o ambiente virtual e instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` local:

```text
TELEGRAM_TOKEN=
GEMINI_API_KEY=
```

Nunca versione credenciais reais.

Execute:

```bash
python bot.py
```

## Possíveis evoluções

- enviar ao modelo contexto conversacional controlado;
- tratar indisponibilidade e erros da API;
- validar configuração obrigatória no startup;
- adicionar testes automatizados;
- separar integração com IA, Telegram e persistência em módulos;
- criar critérios de avaliação mais reproduzíveis.

## Objetivo de aprendizado

O projeto registra minha prática com bots, APIs externas, persistência relacional e integração de IA. As respostas do LLM são feedback gerado por modelo e não uma avaliação objetiva ou certificação da habilidade do candidato.
