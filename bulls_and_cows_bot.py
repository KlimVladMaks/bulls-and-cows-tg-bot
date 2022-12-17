# Необходимые импорты
import telebot
import text
import random

# Токен для подключения бота
bot_token = "token"

# Переменная для хранения глобальной последовательности
sequence: str = ""

# Глобальный счётчик количества попыток
counter = 0

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

        # Обнуляем глобальный счётчик попыток
        global counter
        counter = 0

        # Обновляем глобальную последовательность
        update_sequence()

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

    # Объявляем глобальный счётчик попыток
    global counter

    # Если пользователь вводит "/stop", то выводим заключительное сообщение и не продолжаем игровой цикл
    if message.text == "/stop":
        bot.send_message(message.chat.id, text.userPlay_stop_text)

        # На всякий случай обнуляем глобальный счётчик попыток
        counter = 0

    # Если пользователь ввёл корректный вариант последовательности
    elif check_user_input(message.text, "userPlay_input"):

        # Увеличиваем глобальный счётчик попыток на единицу
        counter += 1

        # Подчитываем количество быков и коров
        bulls, cows = count_bulls_and_cows(message.text)

        # Если пользователь угадал последовательность, то выводим поздравления,
        # обнуляем счётчик и не продолжаем игровой цикл
        if bulls == 4:
            bot.send_message(message.chat.id, f'Поздравляю! Вы угадали загаданную мною последовательность. '
                                              f'Это действительно "{sequence}".\n'
                                              f'\n'
                                              f'Количество затраченных попыток: {counter}')
            bot.send_message(message.chat.id, text.userPlay_stop_text)
            counter = 0
            return

        # Иначе выводим количество быков и коров и продолжаем игровой цикл
        user_input = bot.send_message(message.chat.id, f'{counter}) Быков - {bulls}, Коров - {cows}')
        bot.register_next_step_handler(user_input, user_play)

    # Если пользователь ввёл некорректные данные, то выводим сообщение о некорректном вводе и продолжить игровой цикл
    else:
        user_input = bot.send_message(message.chat.id, text.userPlay_incorrect_input_text)
        bot.register_next_step_handler(user_input, user_play)


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


def update_sequence():
    """
    Обновляем глобальную последовательность случайным образом.
    """

    # Задаём и очищаем глобальную последовательность
    global sequence
    sequence = ""

    # Создаём список из неповторяющихся цифр и перемешиваем его
    numbers_list = list(range(10))
    random.shuffle(numbers_list)

    # Берём из списка четыре элемента и добавляем их в глобальную последовательность
    for i in range(4):
        sequence += str(numbers_list[i])


def count_bulls_and_cows(user_seq: str) -> tuple[int, int]:
    """
    Подчитывает количество быков и коров в пользовательской последовательности.
    :param user_seq: Пользовательская последовательность.
    :return: Кортеж, содержащий количество быков и коров.
    """

    # Счётчики быков и коров
    bulls = 0
    cows = 0

    # Перебираем все цифры пользовательской последовательности и подсчитываем количество быков и коров
    for i in range(4):
        if user_seq[i] == sequence[i]:
            bulls += 1
        elif user_seq[i] in sequence:
            cows += 1

    # Возвращаем число быков и коров
    return bulls, cows


# Запускаем бота в режиме постоянного прослушивания пользовательского ввода
bot.polling(none_stop=True)




