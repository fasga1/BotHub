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
    def get_employee_inline_keyboard_with_finish(employees):
        buttons = []
        for name in employees:
            buttons.append([InlineKeyboardButton(name, callback_data=f"select_{name}")])
        buttons.append([InlineKeyboardButton("Закончить работу", callback_data="finish_bot")])
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def get_style_inline_keyboard(employee_name: str):
        buttons = [
            [InlineKeyboardButton("Официальный", callback_data=f"style_official_{employee_name}")],
            [InlineKeyboardButton("Деловой", callback_data=f"style_business_{employee_name}")],
            [InlineKeyboardButton("Дружеский", callback_data=f"style_friendly_{employee_name}")],
            [InlineKeyboardButton("Назад к списку сотрудников", callback_data="back_to_employees")]
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def get_feedback_inline_keyboard(employee_name: str):
        buttons = [
            [InlineKeyboardButton("Понравилось", callback_data=f"feedback_like_{employee_name}")],
            [InlineKeyboardButton("Внести правки", callback_data=f"feedback_edit_{employee_name}")],
            [InlineKeyboardButton("Полностью переписать", callback_data=f"feedback_rewrite_{employee_name}")]
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def get_like_confirmation_keyboard():
        buttons = [
            [InlineKeyboardButton("Да, вернуться к списку", callback_data="like_yes")],
            [InlineKeyboardButton("Нет, закончить", callback_data="like_no")]
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def get_post_edit_keyboard():
        buttons = [
            [InlineKeyboardButton("К списку сотрудников", callback_data="back_to_employees")],
            [InlineKeyboardButton("Закончить работу", callback_data="finish_bot")]
        ]
        return InlineKeyboardMarkup(buttons)