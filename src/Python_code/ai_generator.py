import os
import requests
import logging
from dotenv import load_dotenv
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenRouterOpenAIGenerator:

    def __init__(self, api_key: str, site_url: str = None, site_name: str = None):
        try:
            from openai import OpenAI
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            self.api_key = api_key
            self.extra_headers = {
                "HTTP-Referer": site_url or "https://localhost",
                "X-Title": site_name or "Telegram Birthday Bot"
            }
            self.site_url = site_url or "https://localhost"
            self.site_name = site_name or "Telegram Birthday Bot"
            logger.info("Инициализирован OpenRouter генератор (openai lib)")
        except ImportError:
            logger.error("❌ Установите библиотеку openai: pip install openai")
            raise

    def generate_congratulation(self, employee_name: str, style_type: str,
                                occasion: str = "день рождения", feedback: str = None) -> Optional[str]:
        from openai import OpenAIError

        style_descriptions = {
            "official": "Официальный, уважительный стиль",
            "business": "Деловой, профессиональный стиль",
            "friendly": "Дружеский, неформальный стиль с эмодзи"
        }

        style_desc = style_descriptions.get(style_type, style_descriptions["business"])

        if feedback:
            prompt = (
                f"Ты приложение для написания поздравлений. В твой ответ должно входить только поздравление. "
                f"Без лишних слов и на русском языке.\n\n"
                f"Исходное поздравление было сгенерировано для '{employee_name}' по поводу '{occasion}' в стиле '{style_desc}'.\n"
                f"Пользователь просит: \"{feedback}\"\n\n"
                f"Напиши обновлённое поздравление, учтя эту правку. 3-4 предложения."
            )
        else:
            prompt = (
                f"Ты приложение для написания поздравлений. В твой ответ должно входить только поздравление. "
                f"Без лишних слов и на русском языке. "
                f"Напиши поздравление с '{occasion}' для '{employee_name}' в '{style_desc}' стиле. 3-4 предложения"
            )

        logger.info(f"Промпт для ИИ:\n{prompt}")
        try:
            completion = self.client.chat.completions.create(
                extra_headers=self.extra_headers,
                model="xiaomi/mimo-v2-flash:free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=150
            )
            return completion.choices[0].message.content.strip()
        except OpenAIError as e:
            logger.error(f"Ошибка OpenAI библиотеки: {e}")
            return None

    def test_connection(self) -> bool:
        from openai import OpenAIError

        try:
            self.client.chat.completions.create(
                extra_headers=self.extra_headers,
                model="xiaomi/mimo-v2-flash:free",
                messages=[{"role": "user", "content": "Привет"}],
                max_tokens=5,
                temperature=0.1
            )
            return True
        except OpenAIError as e:
            logger.error(f"Ошибка теста подключения: {e}")
            return False
        except Exception as e:
            logger.error(f"Неизвестная ошибка теста: {e}")
            return False


def create_openrouter_generator(use_openai_lib: bool = False) -> Optional[OpenRouterOpenAIGenerator]:
    load_dotenv()

    API_KEY = os.getenv("OPENROUTER_API_KEY")

    if not API_KEY:
        logger.error("❌ Не найден OPENROUTER_API_KEY в переменных окружения")
        logger.info("💡 Добавьте в .env файл: OPENROUTER_API_KEY=ваш_ключ")
        logger.info("   Получите ключ на: https://openrouter.ai/keys")
        return None


    try:
        generator = OpenRouterOpenAIGenerator(
            api_key=API_KEY,
        )

        # Тестируем подключение
        if generator.test_connection():
            logger.info("✅ Подключение к OpenRouter успешно")
            return generator
        else:
            logger.error("❌ Не удалось подключиться к OpenRouter API")
            return None
    except Exception as e:
        logger.error(f"❌ Ошибка создания генератора: {e}")
        return None