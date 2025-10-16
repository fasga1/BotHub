from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "8173274497:AAFQppVLPx3LgJi1GdaQHgVOZwj6n8aFTFQ"

async def start(update, context):
    await update.message.reply_text('Привет! Я твой бот 😊')

async def echo(update, context):
    await update.message.reply_text(update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()