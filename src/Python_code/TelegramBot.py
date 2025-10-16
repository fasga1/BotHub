from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

Button_text = "Зарегистрироваться"

async def start(update, context):
    button = KeyboardButton(Button_text)
    keyboard = [[button]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text(
    "Привет!\nВы запустили WB_Congratulations_bot\n\nВот инструкция по пользованию ботом для вас:\n\nПервым делом, для работы в боте вам необходимо зарегистрироваться используя вашу корпаративную почту и выданый вам пароль, для этого нажмите на кнопку 'Зарегистрироваться'",
        reply_markup=reply_markup
    )

async def handle_button(update, context):
    user_text = update.message.text
    if user_text == Button_text:
        await update.message.reply_text("Введите ваш ЛОГИН и ПАРОЛЬ в формате:\n ЛОГИН:{ваша почта}\n ПАРОЛЬ:{ваш пароль}")
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