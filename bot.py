import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
import banco

# Carrega as variáveis do arquivo .env
load_dotenv()

# Inicializa o banco de dados SQLite
banco.iniciar_banco()

# Pega as chaves diretamente do sistema operacional, sem expor no código
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicializa o cliente da IA do Google
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# ... (o restante do código continua exatamente igual)


# Mensagem de Boas-vindas ao digitar /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    texto = (
        f"Olá, {user_name}! Eu sou o seu Simulador de Entrevistas Técnicas. 🧠\n\n"
        "Para começar a treinar, digite um comando escolhendo sua tecnologia:\n"
        "👉 `/entrevista python`\n"
        "👉 `/entrevista java`\n"
        "👉 `/entrevista sql`\n"
        "👉 `/entrevista javascript`\n"
        "👉 `/entrevista c`\n\n"
        "Para encerrar a sessão a qualquer momento, digite `/parar`."
    )
    await update.message.reply_text(texto, parse_mode="Markdown")

# Inicia ou reinicia uma entrevista técnica
# Inicia ou reinicia uma entrevista técnica
async def iniciar_entrevista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Valida se o usuário digitou o argumento do comando
    if not context.args:
        await update.message.reply_text("Por favor, informe a tecnologia. Exemplo: `/entrevista python`", parse_mode="Markdown")
        return
        
    # CORREÇÃO: Pegamos o primeiro item da lista usando [0] antes de transformar em minúsculo
    tecnologia = context.args[0].lower()
    lista_techs = ["python", "java", "sql", "javascript", "c"]
    
    if tecnologia not in lista_techs:
        await update.message.reply_text(f"Tecnologia inválida. Escolha entre: {', '.join(lista_techs)}")
        return

    # Limpa histórico antigo e ativa o estado no banco SQL
    banco.limpar_historico_usuario(user_id)
    banco.atualizar_estado_usuario(user_id, tecnologia, ativa=1)
    
    await update.message.reply_text(f"Iniciando entrevista de *{tecnologia.upper()}*! Estou gerando a primeira pergunta...", parse_mode="Markdown")
    
    # Prompt do sistema para orientar o comportamento da IA
    prompt_sistema = (
        f"Você é um recrutador técnico sênior especialista em {tecnologia}. "
        "Sua tarefa é fazer uma entrevista técnica com um desenvolvedor Júnior. "
        "Faça apenas UMA pergunta teórica ou prática de nível júnior. "
        "Seja direto e aja estritamente como o entrevistador, sem enrolação ou introduções longas. responda em português."
    )
    
    # Chama a API do Gemini
    resposta_ia = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_sistema
    )
    
    # Salva a pergunta gerada no histórico SQL e envia para o chat do Telegram
    banco.salvar_mensagem_historico(user_id, "bot", resposta_ia.text)
    await update.message.reply_text(resposta_ia.text)

# Comando para interromper e resetar a entrevista
async def parar_entrevista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    banco.atualizar_estado_usuario(user_id, None, ativa=0)
    banco.limpar_historico_usuario(user_id)
    await update.message.reply_text("Entrevista encerrada! Seus dados foram limpos. Quando quiser voltar, digite /entrevista.")

# Processa todas as respostas textuais enviadas pelo usuário
async def gerenciar_conversa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto_usuario = update.message.text
    
    # Consulta o SQLite para checar se há uma entrevista em andamento
    tecnologia, ativa = banco.obter_estado_usuario(user_id)
    
    if not ativa:
        await update.message.reply_text("Você não está em uma entrevista activa. Digite `/entrevista python` para começar!", parse_mode="Markdown")
        return

    # Guarda o que o usuário respondeu no banco
    banco.salvar_mensagem_historico(user_id, "user", texto_usuario)
    
    await update.message.reply_text("Avaliando sua resposta... ⏳")
    
    # Prompt estruturado para avaliar a resposta e emendar a próxima pergunta
    prompt_ia = (
        f"Você é o recrutador sênior de {tecnologia}. O candidato respondeu à pergunta anterior. "
        f"Analise a resposta dele de forma construtiva em português (indique de forma direta o que está certo e o que faltou). "
        "Em seguida, faça a próxima pergunta técnica de nível júnior. Responda em português."
        f"Resposta do candidato: {texto_usuario}"
    )
    
    resposta_ia = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_ia
    )
    
    # Salva o retorno do bot no banco e envia ao usuário
    banco.salvar_mensagem_historico(user_id, "bot", resposta_ia.text)
    await update.message.reply_text(resposta_ia.text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Mapeamento de comandos e mensagens
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("entrevista", iniciar_entrevista))
    app.add_handler(CommandHandler("parar", parar_entrevista))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gerenciar_conversa))

    print("Bot com Gemini rodando com sucesso!")
    app.run_polling()

if __name__ == "__main__":
    main()
