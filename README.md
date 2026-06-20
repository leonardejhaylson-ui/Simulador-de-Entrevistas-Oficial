# Simulador de Entrevistas Tecnicas para Desenvolvedores

Este projeto consiste em um bot para o Telegram desenvolvido em Python que simula entrevistas tecnicas de nivel junior. Utilizando engenharia de prompt e processamento de linguagem natural, o sistema atua como um avaliador para as linguagens Java, Python, SQL, JavaScript e C.

## Funcionalidades Principais
* **Simulacao Dinamica**: O sistema gera perguntas teoricas ou praticas de acordo com a tecnologia selecionada pelo usuario.
* **Avaliacao e Feedback**: O motor de inteligencia artificial analisa a resposta enviada, indicando pontos corretos, omissoes e melhorias tecnicas.
* **Persistencia de Dados**: Armazenamento do estado da sessao e do historico de mensagens em banco de dados relacional.
* **Segurança de Credenciais**: Isolamento completo de tokens de API do Telegram e chaves de acesso externas por meio de variaveis de ambiente.

## Arquitetura e Tecnologias
* **Linguagem**: Python 3
* **Interface de Comunicacao**: Biblioteca python-telegram-bot (implementacao assincrona)
* **Processamento de Linguagem Natural**: SDK google-genai (modelo gemini-2.5-flash)
* **Banco de Dados**: SQLite3 (gerenciamento nativo de tabelas relacionais)
* **Configuraçao**: python-dotenv

## Estrutura do Banco de Dados
O esquema do banco de dados SQLite (`entrevistas.db`) é composto por duas tabelas:
1. `usuarios`: Registra o identificador do usuario, a tecnologia ativa na sessao e o status atual da entrevista.
2. `historico_entrevistas`: Armazena a cronologia das interacoes (perguntas do avaliador e respostas do candidato) para manter a consistencia do contexto enviado à API.

## Instruçoes para Execuçao Local

1. **Clonar o Repositorio**:
   ```bash
   git clone https://github.com/leonardejhaylson-ui/Simulador-de-Entrevistas-Oficial.git
   cd Simulador-de-Entrevistas-Oficial
   ```

2. **Configurar o Ambiente Virtual**:
   ```bash
   python -m venv .venv
   # No Windows:
   .venv\Scripts\activate
   ```

3. **Instalar Dependencias**:
   ```bash
   pip install python-telegram-bot google-genai python-dotenv
   ```

4. **Definir as Variaveis de Ambiente**:
   Crie um arquivo chamado `.env` na raiz do projeto e insira as credenciais:
   ```text
   TELEGRAM_TOKEN=insira_o_token_do_telegram
   GEMINI_API_KEY=insira_a_chave_do_gemini
   ```

5. **Executar a Aplicaçao**:
   ```bash
   python bot.py
   ```

---
Projeto de portfólio focado em integraçao de APIs, persistencia relacional e desenvolvimento de backend.
