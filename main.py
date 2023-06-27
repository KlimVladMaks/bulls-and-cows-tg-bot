# Импорты библиотек
import telebot
import random

# Импорты файлов
import get_token
import text
from bot_chat_session import BotChatSession

# Словарь для хранения сессий пользователей
chat_dict: dict[int, BotChatSession] = {}

# Токен для подключения бота
bot_token = get_token.TOKEN

# Создаём бота
bot = telebot.TeleBot(bot_token)


@bot.message_handler(content_types=["text"])
def processing(message: telebot.types.Message):
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


# Запускаем бота в режиме постоянного прослушивания пользовательского ввода
if __name__ == "__main__":
    print("Telegram-бот запущен...")
    bot.infinity_polling()
