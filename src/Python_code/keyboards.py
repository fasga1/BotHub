from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

class KeyboardManager:
    REGISTER = "Зарегистрироваться"

    @staticmethod
    def get_register_button():
        button = KeyboardButton(KeyboardManager.REGISTER)
        return ReplyKeyboardMarkup([[button]], resize_keyboard=True)

    @staticmethod
    def remove_keyboard():
        return ReplyKeyboardRemove()

    # НОВОЕ: inline-кнопки для выбора сотрудника
    @staticmethod
    def get_employee_inline_keyboard(employees):
        buttons = []
        for name in employees:
            # callback_data — уникальный идентификатор (можно использовать имя или ID)
            buttons.append([InlineKeyboardButton(name, callback_data=f"select_{name}")])
        return InlineKeyboardMarkup(buttons)