# Необходимые импорты
import telebot
import text
import random

# Токен для подключения бота
bot_token = "token"

# Переменная для хранения глобальной последовательности
sequence: str = ""

# Глобальный набор последовательностей
sequence_set: list[str] = []

# Глобальный счётчик количества попыток пользователя
counter_user = 0

# Глобальный счётчик количества попыток бота
counter_bot = 0

# Глобальная переменная, показывающая, запускается ли функция bot_play() впервые
is_start_bot_play = True

# Глобальная переменная для хранения последней последовательности, предложенной ботом
last_bot_seq: str = ""

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
        global counter_user
        counter_user = 0

        # Обновляем глобальную последовательность
        update_sequence()

        # Выводим стартовое сообщение для userPlay-цикла и считываем пользовательский ввод
        user_input = bot.send_message(message.chat.id, text.userPlay_start_text)

        # Переходим к функции, реализующей userPlay-цикл
        bot.register_next_step_handler(user_input, user_play)

    # Если пользователь вводит "/botPlay", то запускаем соответсвующий игровой цикл
    elif message.text == "/botPlay":

        # Обнуляем глобальный счётчик попыток
        global counter_bot
        counter_bot = 0

        # Показываем, что функция bot_play() запускается впервые
        global is_start_bot_play
        is_start_bot_play = True

        # Обновляем глобальный список последовательностей
        fill_sequence_set()

        # Выводим стартовое сообщение для botPlay-цикла
        bot.send_message(message.chat.id, text.botPlay_start_text)

        # Запускаем игровой цикл
        bot_play(message)

    # Если пользователь ввёл некорректные данные, то вывести сообщение о некорректном вводе
    else:
        bot.send_message(message.chat.id, text.incorrect_input_text)


def user_play(message):
    """
    Игровой цикл, когда пользователь отгадывает последовательность, загаданную ботом.
    :param message: Сообщение пользователя.
    """

    # Объявляем глобальный счётчик попыток
    global counter_user

    # Если пользователь вводит "/stop", то выводим заключительное сообщение и не продолжаем игровой цикл
    if message.text == "/stop":
        bot.send_message(message.chat.id, text.userPlay_stop_text)

        # На всякий случай обнуляем глобальный счётчик попыток
        counter_user = 0

    # Если пользователь ввёл корректный вариант последовательности
    elif check_user_input(message.text, "userPlay_input"):

        # Увеличиваем глобальный счётчик попыток на единицу
        counter_user += 1

        # Подчитываем количество быков и коров
        bulls, cows = count_bulls_and_cows(message.text)

        # Если пользователь угадал последовательность, то выводим поздравления,
        # обнуляем счётчик и не продолжаем игровой цикл
        if bulls == 4:
            bot.send_message(message.chat.id, f'Поздравляю! Вы угадали загаданную мною последовательность. '
                                              f'Это действительно "{sequence}".\n'
                                              f'\n'
                                              f'Количество затраченных попыток: {counter_user}')
            bot.send_message(message.chat.id, text.userPlay_stop_text)
            counter_user = 0
            return

        # Иначе выводим количество быков и коров и продолжаем игровой цикл
        user_input = bot.send_message(message.chat.id, f'{counter_user}) Быков - {bulls}, Коров - {cows}')
        bot.register_next_step_handler(user_input, user_play)

    # Если пользователь ввёл некорректные данные, то выводим сообщение о некорректном вводе и продолжаем игровой цикл
    else:
        user_input = bot.send_message(message.chat.id, text.userPlay_incorrect_input_text)
        bot.register_next_step_handler(user_input, user_play)


def bot_play(message):
    """
    Игровой цикл, когда бот отгадывает последовательность, загаданную пользователем.
    :param message: Сообщение пользователя.
    :param is_start: Является ли вызов функции первым.
    """

    # Объявляем глобальный счётчик попыток
    global counter_bot

    # Объявляем глобальный показатель первого запуска
    global is_start_bot_play

    # Объявляем переменную для хранения последней предложенной последовательности
    global last_bot_seq

    # Если функция запускается впервые
    if is_start_bot_play:

        # Показываем, что функция уже была запущена
        is_start_bot_play = False

        # Увеличиваем счётчик попыток на один
        counter_bot += 1

        # Выбираем случайную последовательность из списка
        last_bot_seq = random.choice(sequence_set)

        # Удаляем выбранную последовательность из списка
        sequence_set.remove(last_bot_seq)

        # Выводим выбранную последовательность пользователю и считываем ответ
        user_input = bot.send_message(message.chat.id, f"{counter_bot}) Мой вариант: {last_bot_seq}")

        # Запускаем новый игровой цикл
        bot.register_next_step_handler(user_input, bot_play)

    # Если пользователь вводит "/stop", то выводим заключительное сообщение и не продолжаем игровой цикл
    elif message.text == "/stop":
        bot.send_message(message.chat.id, text.userPlay_stop_text)

        # На всякий случай обнуляем глобальный счётчик попыток
        counter_bot = 0

    # Если пользователь корректно ввёл число угаданных быков и коров
    elif check_user_input(message.text, "botPlay_input"):

        # Выделяем число быков и коров
        bull_count, cow_count = int(message.text[0]), int(message.text[2])

        # Если бот угадал последовательность, то выводим сопутствующие сообщения,
        # обнуляем счётчик и прерываем игровой цикл
        if bull_count == 4:
            bot.send_message(message.chat.id, f'Ура, я угадал! Неужели это действительно была '
                                              f'последовательность "{last_bot_seq}"?! Какой же я молодец!\n'
                                              f'\n'
                                              f'Количество затраченных попыток: {counter_bot}')
            bot.send_message(message.chat.id, text.userPlay_stop_text)
            counter_bot = 0
            return

        # Очищаем глобальный список переменных от неподходящих значений
        thin_out_sequence_set(last_bot_seq, bull_count, cow_count)

        # Если у бота закончились варианты, то выводим сообщение об ошибке и прерываем игровой цикл
        if len(sequence_set) == 0:
            bot.send_message(message.chat.id, text.botPlay_empty_list_error_text)
            bot.send_message(message.chat.id, text.userPlay_stop_text)
            return

        # Увеличиваем счётчик попыток на один
        counter_bot += 1

        # Выбираем случайную последовательность из списка
        last_bot_seq = random.choice(sequence_set)

        # Удаляем выбранную последовательность из списка
        sequence_set.remove(last_bot_seq)

        # Выводим выбранную последовательность пользователю и считываем ответ
        user_input = bot.send_message(message.chat.id, f"{counter_bot}) Мой вариант: {last_bot_seq}")

        # Запускаем новый игровой цикл
        bot.register_next_step_handler(user_input, bot_play)

    # Если пользователь ввёл некорректные данные, то выводим сообщение о некорректном вводе и продолжаем игровой цикл
    else:
        user_input = bot.send_message(message.chat.id, text.botPlay_incorrect_input_text)
        bot.register_next_step_handler(user_input, bot_play)


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

    # При проверке для ввода в botPlay-цикле, проверяем, что пользователь ввёл корректное количество быков и коров
    # и выводим соответствующий результат
    elif check_type == "botPlay_input":
        if ((len(user_input) == 3)
                and (user_input[0] in "01234")
                and (user_input[1] == " ")
                and (user_input[2] in "01234")
                and (int(user_input[0]) + int(user_input[2]) <= 4)):
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


def fill_sequence_set():
    """
    Заполняем глобальный список последовательностей всеми допустимыми последовательностями.
    """

    # Инициализируем список последовательностей
    global sequence_set

    # На всякий случай очищаем список последовательностей
    sequence_set.clear()

    # Перебираем все возможные числа последовательности
    for n1 in range(10):
        for n2 in range(10):
            for n3 in range(10):
                for n4 in range(10):

                    # Собираем новую последовательность
                    new_seq = str(n1) + str(n2) + str(n3) + str(n4)

                    # Если последовательность корректна, то добавляем её в список
                    # (Для проверки используем функцию проверки пользовательского ввода)
                    if check_user_input(new_seq, "userPlay_input"):
                        sequence_set.append(new_seq)


def count_bulls_and_cows(user_seq: str, true_seq=sequence) -> tuple[int, int]:
    """
    Подчитывает количество быков и коров в пользовательской последовательности.
    :param true_seq: Последовательность, для которой нужно посчитать число угаданных быков и коров
    (по умолчанию используется глобальная последовательность).
    :param user_seq: Пользовательская последовательность.
    :return: Кортеж, содержащий количество быков и коров.
    """

    # Счётчики быков и коров
    bulls = 0
    cows = 0

    # Перебираем все цифры пользовательской последовательности и подсчитываем количество быков и коров
    for i in range(4):
        if user_seq[i] == true_seq[i]:
            bulls += 1
        elif user_seq[i] in true_seq:
            cows += 1

    # Возвращаем число быков и коров
    return bulls, cows


def thin_out_sequence_set(proven_seq: str, bull_count: int, cow_count):
    """
    Отсеивает из глобального списка последовательности, неподходящие к указанному пользователю
    количеству "быков" и "коров".
    :param proven_seq: Последовательность, для которой пользователь указал число "быков" и "коров".
    :param bull_count: Количество угаданных "быков".
    :param cow_count: Количество угаданных "коров".
    """

    # Объявляем глобальный список последовательностей
    global sequence_set

    # Создаём копию глобального списка последовательностей
    sequence_set_copy = sequence_set.copy()

    # Перебираем все последовательности из глобального списка
    for seq in sequence_set_copy:

        # Подчитываем число быков и коров относительно заданной последовательности
        bull_count_in_seq, cow_count_in_seq = count_bulls_and_cows(seq, proven_seq)

        # Если число быков и коров не совпадает с таковыми у переданной последовательности,
        # то удаляем итерируемую последовательность из глобального списка
        if (bull_count_in_seq != bull_count) or (cow_count_in_seq != cow_count):
            sequence_set.remove(seq)


# Запускаем бота в режиме постоянного прослушивания пользовательского ввода
bot.polling(none_stop=True)



