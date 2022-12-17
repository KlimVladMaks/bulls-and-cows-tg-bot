# Необходимые импорты
import telebot
import text

# Токен для подключения бота
bot_token = "токен"

# Создаём бота
bot = telebot.TeleBot(bot_token)


# Активируется при текстовом вводе пользователя
@bot.message_handler(content_types=["text"])
def processing(message):
    """
    Обработка основных пользовательских команд.
    :param message: Класс пользовательского сообщения.
    """

    # Если пользователь вводит "/start", то выводим приветственное сообщение
    if message.text == "/start":
        bot.send_message(message.chat.id, text.start_text)

    # Если пользователь вводит "/help", то вывести сообщение со справочной информацией
    elif message.text == "/help":
        bot.send_message(message.chat.id, text.help_text)

    # Если пользователь вводит "/rules", то вывести сообщение с правилами игры
    elif message.text == "/rules":
        bot.send_message(message.chat.id, text.rules_text)

    # Если пользователь вводит "/userPlay", то запускаем соответсвующий игровой цикл
    elif message.text == "/userPlay":

        # Выводим стартовое сообщение для userPlay-цикла и считываем пользовательский ввод
        user_input = bot.send_message(message.chat.id, text.userPlay_start_text)

        # Переходим к функции, реализующей userPlay-цикл
        bot.register_next_step_handler(user_input, user_play)

    # Если пользователь ввёл некорректные данные, то вывести сообщение о некорректном вводе
    else:
        bot.send_message(message.chat.id, text.incorrect_input_text)


def user_play(message):
    """
    Игровой цикл, когда пользователь отгадывает последовательность, загаданную ботом.
    :param message: Сообщение пользователя.
    """

    # Если пользователь вводит "/stop", то выводим заключительное сообщение и не продолжаем игровой цикл
    if message.text == "/stop":
        bot.send_message(message.chat.id, text.userPlay_stop_text)

    elif check_user_input(message.text, "userPlay_input"):
        pass


def check_user_input(user_input: str, check_type: str) -> bool:
    """
    Проверка пользовательского ввода на корректность.
    :param user_input: Строка, введённая пользователем.
    :param check_type: Тип требуемой проверки
    :return: True - если ввод корректен, False - если ввод некорректен.
    """

    # При проверке для ввода в userPlay-цикле, проверяем, что пользователь ввёл последовательность
    # из четырёх неповторяющихся цифр, и выводим соответсвующий результат.
    if check_type == "userPlay_input":
        if (len(user_input) == 4) and (user_input.isdigit()) and (len(set(user_input)) == len(user_input)):
            return True
        else:
            return False


# Запускаем бота в режиме постоянного прослушивания пользовательского ввода
bot.polling(none_stop=True)




