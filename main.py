# Импорты библиотек
import telebot
import datetime

# Импорты файлов
from bot_chat_session import BotChatSession

# Переменная для хранения бота
bot: telebot.TeleBot

# При запуске программы
if __name__ == "__main__":

    # Цикл проверки корректности токена
    while True:

        # Запрашиваем токен и создаём бота
        bot_token = input("Введите токен для Telegram-бота:\n")
        bot = telebot.TeleBot(token=bot_token)

        # Проверяем корректность токена
        # (Если токен корректен - выходим из цикла, иначе - повторяем цикл)
        try:
            bot_info = bot.get_me()
        except:
            print("Не удаётся подключиться к Telegram-боту. Проверьте правильность токена и введите его повторно.")
            continue
        else:
            print("Подключение к Telegram-боту успешно установлено.")
            break

# Словарь для хранения сессий пользователей
chat_dict: dict[int, BotChatSession] = {}


@bot.message_handler(content_types=["text"])
def message_handler(message: telebot.types.Message):
    """
    Функция для обработки пользовательского ввода.

    :param message: Сообщение пользователя, содержащее текст ввода.
    """
    
    # Если ID данного чата не содержится в списке текущих сессий, то создаём новую сессию для данного чата
    if message.chat.id not in chat_dict:
        chat_dict[message.chat.id] = BotChatSession()

    # Отправляем боту сообщение пользователя и получаем список с ответами на него
    bot_outputs: list[str] = chat_dict[message.chat.id].processing(message.text)

    # Перебираем все ответы бота и отправляем их в чат пользователю
    for bot_output in bot_outputs:
        bot.send_message(message.chat.id, bot_output)


# При запуске программы
if __name__ == "__main__":

    # Выводим сообщение о запуске бота
    print("Telegram-бот запущен...")

    # Запускаем бесконечный цикл работы бота
    while True:

        # Запускаем бота в режиме постоянного мониторинга
        try:
            bot.polling(non_stop=True)
        
        # При возникновении исключения, выводим сообщение об ошибке и повторяем цикл
        except Exception:
            print(f"{datetime.datetime.now()}: Соединение с Telegram-ботом нестабильно. Возможны задержки при ответе " \
                  f"на сообщения пользователей или их потеря.")
            continue

        # Иначе просто повторяем цикл
        else:
            continue
