from yandex_cloud_ml_sdk import YCloudML

def ask_yagpt(question,temperature):
    temperature = 0.5
    sdk = YCloudML(
        folder_id="",
        auth="",
    )
    model = sdk.models.completions("yandexgpt")
    model = model.configure(temperature=temperature)

    result = model.run(question)

    if not result.alternatives:
        return "⚠️ Не получилось сгенерировать ответ"

    response = result.alternatives[0].text

    # Красивый вывод результатов
    print("\n" + "=" * 50)
    print(f"📋 ВОПРОС: {question}")
    print("=" * 50)
    print(f"🤖 ОТВЕТ: {response}")
    print("=" * 50)
    print("📊 ДЕТАЛИ ОТВЕТА:")
    print(f"- Статус: {result.alternatives[0].status.name}")
    print(f"- Модель: {result.model_version}")
    print(f"- Использовано токенов: {result.usage.total_tokens}")
    print("=" * 50 + "\n")

    return response

if __name__ == "__main__":
    response = ask_yagpt("Что такое гора?",temperature=0.5)
    print(response)
