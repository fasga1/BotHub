from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
import os
from dotenv import load_dotenv
from keyboards import KeyboardManager
from states import LOGIN, PASSWORD

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

user_data = {}

async def start(update, context):
    reply_markup = KeyboardManager.get_register_button()  # 👈 Вызываем метод из класса
    await update.message.reply_text(
        "Привет!\nВы запустили WB_Congratulations_bot\n\n"
        "Вот инструкция по пользованию ботом для вас:\n\n"
        "Первым делом, для работы в боте вам необходимо зарегистрироваться, "
        "используя вашу корпоративную почту и выданный вам пароль. "
        "Для этого нажмите на кнопку 'Зарегистрироваться'",
        reply_markup=reply_markup
    )

async def handle_button(update, context):
    user_text = update.message.text
    if user_text == KeyboardManager.REGISTER:  # 👈 Сравниваем с константой из класса
        await update.message.reply_text(
            "Введите ваш ЛОГИН и ПАРОЛЬ в формате:\n"
            "ЛОГИН:{ваша почта}\n"
            "ПАРОЛЬ:{ваш пароль}"
        )
    else:
        await update.message.reply_text("Я понимаю только кнопку!")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))

    print("Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()