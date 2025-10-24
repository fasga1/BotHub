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

    @staticmethod
    def get_employee_inline_keyboard(employees):
        buttons = []
        for name in employees:
            # callback_data — уникальный идентификатор (можно использовать имя или ID)
            buttons.append([InlineKeyboardButton(name, callback_data=f"select_{name}")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def get_style_inline_keyboard(employee_name: str):
        buttons = [
            [InlineKeyboardButton("Официальный", callback_data=f"style_official_{employee_name}")],
            [InlineKeyboardButton("Деловой", callback_data=f"style_business_{employee_name}")],
            [InlineKeyboardButton("Дружеский", callback_data=f"style_friendly_{employee_name}")]
        ]
        return InlineKeyboardMarkup(buttons)