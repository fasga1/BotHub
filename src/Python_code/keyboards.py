from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

class KeyboardManager:
    REGISTER = "Зарегистрироваться"

    @staticmethod
    def get_register_button():
        button = KeyboardButton(KeyboardManager.REGISTER)
        return ReplyKeyboardMarkup([[button]], resize_keyboard=True)

    @staticmethod
    def remove_keyboard():
        return ReplyKeyboardRemove()