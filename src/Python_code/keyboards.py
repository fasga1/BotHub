from telegram import ReplyKeyboardMarkup, KeyboardButton

class KeyboardManager:
    REGISTER = "Зарегистрироваться"

    @staticmethod
    def get_register_button():
        button = KeyboardButton(KeyboardManager.REGISTER)
        return ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=False)