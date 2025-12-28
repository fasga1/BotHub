from src.Python_code.ai_generator import create_openrouter_generator


def main():
    print("🧪 Тестирование OpenRouter генератора")
    print("=" * 50)

    generator = create_openrouter_generator(use_openai_lib=True)

    if not generator:
        print("\n❌ Не удалось создать генератор. Проверьте:")
        print("   1. Файл .env в той же папке")
        print("   2. Содержимое .env: OPENROUTER_API_KEY=ваш_ключ")
        print("   3. Получите ключ на: https://openrouter.ai/keys")
        exit(1)

    test_cases = [
        ("Анна", "friendly", "день рождения"),
        ("Иван Петрович", "official", "юбилей работы"),
        ("Мария", "business", "повышение"),
    ]

    print(f"\n🔗 Подключение установлено. Ключ: {generator.api_key[:10]}...")
    print(f"🌐 Сайт: {generator.site_url}")
    print(f"🤖 Используемая модель: tngtech/deepseek-r1t-chimera:free")
    print(f"📊 Тестируем {len(test_cases)} сценариев:\n")

    successful = 0
    for i, (name, style, occasion) in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"Тест #{i}: {name} | Стиль: {style} | Повод: {occasion}")
        print('=' * 60)

        congratulations = generator.generate_congratulation(
            employee_name=name,
            style_type=style,
            occasion=occasion
        )

        if congratulations:
            successful += 1
            print(f"✅ УСПЕХ:\n{congratulations}")
        else:
            print(f"❌ НЕ УДАЛОСЬ СГЕНЕРИРОВАТЬ")

    print(f"\n📈 Результаты: {successful}/{len(test_cases)} успешных генераций")


if __name__ == "__main__":
    main()