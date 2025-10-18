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
import re

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
    return None

async def register_start(update, context):
    await update.message.reply_text(
        "Введите ваш логин (корпоративная почта):",
        reply_markup=KeyboardManager.remove_keyboard()  # ← убираем кнопки
    )
    return LOGIN

CORPORATE_DOMAIN = "st.ithub.ru"  # ← измените на ваш домен

async def get_login(update, context):
    user_login = update.message.text.strip()

    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user_login):
        await update.message.reply_text(
            "Неверный формат email. Попробуйте снова:\n\n"
            "Пример: ivanov@st.ithub.ru"
        )
        return LOGIN

    if not user_login.endswith(f"@{CORPORATE_DOMAIN}"):
        await update.message.reply_text(
            f"Почта должна быть корпоративной (@{CORPORATE_DOMAIN}).\n"
            "Попробуйте снова:"
        )
        return LOGIN

    context.user_data['login'] = user_login
    await update.message.reply_text("Введите ваш пароль:")
    return PASSWORD

async def get_password(update, context):
    user_password = update.message.text.strip()
    context.user_data['password'] = user_password
    await update.message.reply_text("✅ Доступ открыт!")

    context.user_data.clear()

    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text([KeyboardManager.REGISTER]), register_start)],
        states={
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_login)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()