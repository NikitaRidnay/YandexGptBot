import telebot
import time
from yandex_cloud_ml_sdk import YCloudML


TELEGRAM_TOKEN = ""
YANDEX_FOLDER_ID = ""
YANDEX_AUTH_TOKEN = ""

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ask_yagpt(question, temperature=0.5):
    try:
        sdk = YCloudML(
            folder_id=YANDEX_FOLDER_ID,
            auth=YANDEX_AUTH_TOKEN,
        )


        model = sdk.models.completions("yandexgpt")
        model = model.configure(temperature=temperature)


        result = model.run(question)

        if not result.alternatives:
            return "⚠️ Не удалось сгенерировать ответ"

        return result.alternatives[0].text

    except Exception as e:
        print(f"Ошибка при запросе к YandexGPT: {e}")
        return "⛔ Произошла ошибка при обработке запроса"




@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Привет! Я бот с интеграцией YandexGPT.\n\n"
        "Просто задай мне любой вопрос, и я постараюсь на него ответить!\n\n"
        "Также доступны команды:\n"
        "/help - Справка\n"
        "/ask - Задать вопрос"
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "ℹ️ Справка по использованию бота:\n\n"
        "1. Просто напиши вопрос в чат\n"
        "2. Или используй команду /ask с вопросом\n"
        "3. Пример: /ask Что такое черная дыра?\n\n"
        "Бот использует YandexGPT для генерации ответов.\n"
        "Температура генерации: 0.5 (баланс креативности)"
    )
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['ask'])
def handle_ask_command(message):

    question = message.text[len('/ask '):].strip()

    if not question:
        bot.reply_to(message, "❌ Пожалуйста, укажите вопрос после команды\nПример: /ask Что такое Солнце?")
        return

    processing_msg = bot.reply_to(message, "⏳ Обрабатываю ваш запрос...")

    start_time = time.time()

    response = ask_yagpt(question)


    processing_time = time.time() - start_time

    bot.edit_message_text(
        chat_id=processing_msg.chat.id,
        message_id=processing_msg.message_id,
        text=f"❓ Вопрос: {question}\n\n💡 Ответ: {response}\n\n⏱️ Время обработки: {processing_time:.2f} секунд"
    )


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text.startswith('/'):
        return

    processing_msg = bot.reply_to(message, "⏳ Обрабатываю ваш запрос...")
    start_time = time.time()
    response = ask_yagpt(message.text)
    processing_time = time.time() - start_time
    bot.edit_message_text(
        chat_id=processing_msg.chat.id,
        message_id=processing_msg.message_id,
        text=f"💡 Ответ: {response}\n\n⏱️ Время обработки: {processing_time:.2f} секунд"
    )


if __name__ == '__main__':
    bot.polling(none_stop=True)
