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
from database import get_all_employees
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
    employees = get_all_employees()
    await update.message.reply_text(
        "Доступ открыт!\n"
        "Сегодня праздники у нескольких сотрудников.\n"
        "Выберите сотрудника, которого хотите поздравить:",
        reply_markup=KeyboardManager.get_employee_inline_keyboard(employees)
    )
    return ConversationHandler.END

async def show_employees(update: Update, context: ContextTypes.DEFAULT_TYPE):
    employees = get_all_employees()
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text="Сегодня праздники у нескольких сотрудников.\nВыберите сотрудника, которого хотите поздравить:",
            reply_markup=KeyboardManager.get_employee_inline_keyboard(employees)
        )
    else:
        await update.message.reply_text(
            text="Сегодня праздники у нескольких сотрудников.\nВыберите сотрудника, которого хотите поздравить:",
            reply_markup=KeyboardManager.get_employee_inline_keyboard(employees)
        )

async def back_to_employees(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_employees(update, context)

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

    context.user_data['current_employee'] = employee_name
    context.user_data['current_style'] = style_type

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
            "С днём рождения! Желаем море позитива, "
            "крутых идей и чтобы все задачи решались сами! 😎"
        )
    else:
        message = "Неизвестный стиль."

    context.user_data['current_message'] = message

    await query.edit_message_text(
        text=message,
        reply_markup=KeyboardManager.get_feedback_inline_keyboard(employee_name)
    )

async def feedback_like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Отлично! Рады, что вам понравилось!")

async def feedback_rewrite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    employee_name = query.data.split("_", 2)[2]

    await query.edit_message_text(
        text=f"Вы выбрали сотрудника: *{employee_name}*\n\nВыберите стиль поздравления:",
        parse_mode="Markdown",
        reply_markup=KeyboardManager.get_style_inline_keyboard(employee_name)
    )

async def feedback_edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    employee_name = query.data.split("_", 2)[2]

    context.user_data['awaiting_edit'] = True
    context.user_data['current_employee'] = employee_name

    await query.edit_message_text(
        "Пожалуйста, введите вашу версию поздравления:"
    )

async def handle_edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_edit'):
        edited_text = update.message.text.strip()
        employee_name = context.user_data.get('current_employee', 'сотрудник')

        context.user_data['awaiting_edit'] = False

        await update.message.reply_text(
            f"Ваше поздравление для {employee_name}:\n\n{edited_text}\n\n"
            "Отправлено! Спасибо за правки!"
        )
        return

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
    app.add_handler(CallbackQueryHandler(back_to_employees, pattern=r"^back_to_employees"))
    app.add_handler(CallbackQueryHandler(feedback_like, pattern=r"^feedback_like_"))
    app.add_handler(CallbackQueryHandler(feedback_rewrite, pattern=r"^feedback_rewrite_"))
    app.add_handler(CallbackQueryHandler(feedback_edit_start, pattern=r"^feedback_edit_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_text))


    print("Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()