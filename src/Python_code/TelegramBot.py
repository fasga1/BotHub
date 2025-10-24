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
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
load_dotenv()


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

EMPLOYEES = [
    "Анна Петрова",
    "Иван Смирнов",
    "Мария Козлова",
    "Алексей Иванов",
    "Екатерина Соколова"
]

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
    await update.message.reply_text(
        "Доступ открыт!\n"
        "Сегодня праздники у нескольких сотрудников.\n"
        "Выберите сотрудника, которого хотите поздравить:",
        reply_markup=KeyboardManager.get_employee_inline_keyboard(EMPLOYEES)
    )

    return ConversationHandler.END

async def employee_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected_name = query.data.replace("select_", "")

    await query.edit_message_text(
        text=f"Вы выбрали сотрудника: *{selected_name}*\n\n"
             "Выберите стиль поздравления:",
        parse_mode="Markdown",
        reply_markup=KeyboardManager.get_style_inline_keyboard(selected_name)
    )

async def cancel(update, context):
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END

async def style_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_", 2)
    if len(parts) < 3:
        await query.edit_message_text("Ошибка выбора стиля.")
        return

    style_type = parts[1]
    employee_name = parts[2]

    if style_type == "official":
        message = (
            f"Уважаемый(ая) {employee_name}!\n\n"
            "От имени коллектива примите наши искренние поздравления!\n"
            "Желаем крепкого здоровья, профессиональных успехов и благополучия!"
        )
    elif style_type == "business":
        message = (
            f"{employee_name},\n\n"
            "Поздравляем с профессиональным достижением!\n"
            "Ваш вклад в развитие компании высоко ценится. "
            "Успехов в реализации новых проектов!"
        )
    elif style_type == "friendly":
        message = (
            f"Привет, {employee_name}! 🎉\n\n"
            "С днём рождения! Желаю море позитива, "
            "крутых идей и чтобы все задачи решались сами! 😎"
        )
    else:
        message = "Неизвестный стиль."

    await query.edit_message_text(
        text=message
    )


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
    app.add_handler(CallbackQueryHandler(employee_selected, pattern=r"^select_"))
    app.add_handler(CallbackQueryHandler(style_selected, pattern=r"^style_"))

    print("Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()