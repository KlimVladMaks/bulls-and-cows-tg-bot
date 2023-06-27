# Импорт библиотек
import random

# Импорты файлов
import text


class BotChatSession:
    """"
    Класс для реализации сессии бота с одним чатом пользователя.
    (Это позволяет использовать бота в многопользовательском режиме).
    """
    
    def __init__(self) -> None:
        """
        Функция для инициализации сессии с пользователем.

        :param bot: Экземпляр бота.
        :param chat_id: Идентификатор чата с пользователем.
        """

        # Переменная с текущим циклом бота (по-умолчанию указан основной main-цикл)
        self.current_cycle: str = "main"
        
        # Переменная для хранения последовательности, которую пользователь должен отгадать
        self.sequence: str = ""

        # Набор последовательностей
        self.sequence_set: list[str] = []

        # Счётчик количества попыток пользователя
        self.counter_user = 0

        # Счётчик количества попыток бота
        self.counter_bot = 0

        # Переменная, показывающая, запускается ли функция bot_play() впервые
        self.is_start_bot_play = True

        # Переменная для хранения последней последовательности, предложенной ботом
        self.last_bot_seq: str = ""

    def processing(self, user_message_text: str) -> list[str]:
        """
        Функция для обработки пользовательского ввода.

        :param user_message_text: Строка, содержащая сообщение пользователя.
        :return: Список, содержащий строки с ответами бота.
        """
        
        # Основной main-цикл
        if self.current_cycle == "main":

            # При начале сессии с ботом, возвращаем приветственное сообщение
            if user_message_text == "/start":
                return [text.start_text]
            
            # При запросе справки, возвращаем справочное сообщение
            elif user_message_text == "/help":
                return [text.help_text]
            
            # При запросе правил игры, возвращаем сообщение с правилами игры
            elif user_message_text == "/rules":
                return [text.rules_text]

            # Если пользователь хочет сам отгадывать число
            elif user_message_text == "/user_play":
                
                # Переключаемся на цикл user_play
                self.current_cycle = "user_play"

                # Повторяем обработку пользовательского ввода
                return self.processing(user_message_text)

            # Если пользователь хочет, чтобы бот отгадывал число
            elif user_message_text == "/bot_play":
                
                # Переключаемся на цикл bot_play
                self.current_cycle = "bot_play"

                # Повторяем обработку пользовательского ввода
                return self.processing(user_message_text)

            # Если не удалось обработать ввод пользователя, выводим сообщение об ошибке
            else:
                return [text.incorrect_input_text]

        # Цикл user_play (бот загадывает число, игрок - отгадывает)
        elif self.current_cycle == "user_play":
            
            # Запуск цикла
            if user_message_text == "/user_play":

                # Обнуляем счётчик попыток пользователя
                self.counter_user = 0

                # Обновляем последовательность, которую пользователь должен отгадать
                self.update_sequence()

                # Выводим приветственное сообщение
                return [text.user_play_start_text]
            
            # При выходе из цикла
            elif user_message_text == "/stop":
                
                # Переключаемся на main-цикл
                self.current_cycle = "main"

                # Возвращаем финальное сообщение
                return [text.user_play_stop_text]

            # Если ввод пользователя корректен (четыре различные цифры)
            elif self.check_user_input(user_message_text, "user_play_input"):
                
                # Увеличиваем счётчик попыток игрока на один
                self.counter_user += 1

                # Подчитываем количество быков и коров
                bulls, cows = self.count_bulls_and_cows(user_message_text, self.sequence)

                # Если пользователь угадал последовательность, то выводим поздравления,
                # обнуляем счётчик и не возвращаемся в main-цикл
                if bulls == 4:
                    self.current_cycle = "main"
                    self.counter_user = 0
                    bot_outputs = [text.user_play_win_text.format(sequence=self.sequence, 
                                                                 counter_user=self.counter_user)]
                    bot_outputs.append(text.user_play_stop_text)
                    return bot_outputs
                
                # Иначе выводим количество быков и коров
                return [text.user_play_result_text.format(counter_user=self.counter_user, bulls=bulls, cows=cows)]

            # Если не удалось распознать ввод пользователя, выводим сообщение об ошибке
            else:
                return [text.user_play_incorrect_input_text]

        # Цикл bot_play (пользователь загадывает число, бот - отгадывает)
        elif self.current_cycle == "bot_play":
            
            # Запуск цикла
            if user_message_text == "/bot_play":

                # Обнуляем счётчик попыток бота
                self.counter_bot = 0

                # Восстанавливаем список последовательностей
                self.fill_sequence_set()

                # Загружаем приветственное сообщение
                bot_outputs = [text.bot_play_start_text]

                # Увеличиваем счётчик попыток бота на один
                self.counter_bot += 1

                # Выбираем случайную последовательность из списка
                self.last_bot_seq = random.choice(self.sequence_set)

                # Удаляем выбранную последовательность из списка
                self.sequence_set.remove(self.last_bot_seq)

                # Загружаем сообщение с вариантом бота
                bot_outputs.append(text.bot_play_option_text.format(counter_bot=self.counter_bot, 
                                                                    last_bot_seq=self.last_bot_seq))
                
                # Возвращаем сообщения бота
                return bot_outputs

            # Если пользователь хочет завершить игру
            elif user_message_text == "/stop":

                # Возвращаемся в main-цикл
                self.current_cycle = "main"

                # Возвращаем финальное сообщение
                return [text.bot_play_stop_text]

            # Если ввод пользователя корректен
            elif self.check_user_input(user_message_text, "bot_play_input"):
                
                # Выделяем число быков и коров
                bull_count, cow_count = int(user_message_text[0]), int(user_message_text[2])

                # Если бот угадал последовательность, то выводим сопутствующие сообщения, обнуляем счётчик и 
                # возвращаемся в main-цикл
                if bull_count == 4:
                    self.current_cycle = "main"
                    bot_outputs = [text.bot_play_win_text.format(last_bot_seq=self.last_bot_seq, 
                                                                 counter_bot=self.counter_bot)]
                    bot_outputs.append(text.bot_play_stop_text)
                    self.counter_bot = 0
                    return bot_outputs
                
                # Очищаем список последовательностей от неподходящих значений
                self.thin_out_sequence_set(self.last_bot_seq, bull_count, cow_count)

                # Если у бота закончились варианты, то выводим сообщение об ошибке и возвращаемся в main-цикл
                if len(self.sequence_set) == 0:
                    self.current_cycle = "main"
                    bot_outputs = [text.bot_play_empty_list_error_text]
                    bot_outputs.append(text.bot_play_stop_text)
                    return bot_outputs

                # Увеличиваем счётчик попыток бота на один
                self.counter_bot += 1

                # Выбираем случайную последовательность из списка
                self.last_bot_seq = random.choice(self.sequence_set)

                # Удаляем выбранную последовательность из списка
                self.sequence_set.remove(self.last_bot_seq)

                # Возвращаем сообщение с выбранной ботом последовательностью
                return [text.bot_play_option_text.format(counter_bot=self.counter_bot, last_bot_seq=self.last_bot_seq)]

            # Если не удалось распознать ввод пользователя, выводим сообщение об ошибке
            else:
                return [text.bot_play_incorrect_input_text]

    def check_user_input(self, user_input: str, check_type: str) -> bool:
        """
        Проверка пользовательского ввода на корректность.

        :param user_input: Строка, введённая пользователем.
        :param check_type: Тип требуемой проверки
        :return: True - если ввод корректен, False - если ввод некорректен.
        """

        # При проверке для ввода в user_play-цикле, проверяем, что пользователь ввёл последовательность
        # из четырёх неповторяющихся цифр, и выводим соответствующий результат.
        if check_type == "user_play_input":
            if (len(user_input) == 4) and (user_input.isdigit()) and (len(set(user_input)) == len(user_input)):
                return True
            else:
                return False

        # При проверке для ввода в bot_play-цикле, проверяем, что пользователь ввёл корректное количество быков и коров
        # и выводим соответствующий результат
        elif check_type == "bot_play_input":
            if ((len(user_input) == 3)
                    and (user_input[0] in "01234")
                    and (user_input[1] == " ")
                    and (user_input[2] in "01234")
                    and (int(user_input[0]) + int(user_input[2]) <= 4)):
                return True
            else:
                return False

    def update_sequence(self) -> None:
        """
        Функция для обновления последовательности, которую пользователь должен отгадать, случайным образом.
        """

        # Очищаем последовательность
        self.sequence = ""

        # Создаём список из неповторяющихся цифр и перемешиваем его
        numbers_list = list(range(10))
        random.shuffle(numbers_list)

        # Берём из списка четыре элемента и добавляем их в последовательность
        for i in range(4):
            self.sequence += str(numbers_list[i])
  
    def count_bulls_and_cows(self, user_seq: str, true_seq: str) -> tuple[int, int]:
        """
        Функция для подсчёта количества быков и коров в пользовательской последовательности.

        :param true_seq: Последовательность, для которой нужно посчитать число угаданных быков и коров.
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

    def fill_sequence_set(self) -> None:
        """
        Функция для заполнения списка последовательностей всеми допустимыми последовательностями.
        """

        # На всякий случай очищаем список последовательностей
        self.sequence_set.clear()

        # Перебираем все возможные числа последовательности
        for n1 in range(10):
            for n2 in range(10):
                for n3 in range(10):
                    for n4 in range(10):

                        # Собираем новую последовательность
                        new_seq = str(n1) + str(n2) + str(n3) + str(n4)

                        # Если последовательность корректна, то добавляем её в список
                        # (Для проверки используем функцию проверки пользовательского ввода)
                        if self.check_user_input(new_seq, "user_play_input"):
                            self.sequence_set.append(new_seq)

    def thin_out_sequence_set(self, proven_seq: str, bull_count: int, cow_count) -> None:
        """
        Функция для отсеивания из списка последовательностей тех, которые не подходят к указанному пользователю
        количеству "быков" и "коров".

        :param proven_seq: Последовательность, для которой пользователь указал число "быков" и "коров".
        :param bull_count: Количество угаданных "быков".
        :param cow_count: Количество угаданных "коров".
        """

        # Создаём копию списка последовательностей
        sequence_set_copy = self.sequence_set.copy()

        # Перебираем все последовательности из списка
        for seq in sequence_set_copy:

            # Подчитываем число быков и коров относительно заданной последовательности
            bull_count_in_seq, cow_count_in_seq = self.count_bulls_and_cows(seq, proven_seq)

            # Если число быков и коров не совпадает с таковыми у переданной последовательности,
            # то удаляем итерируемую последовательность из списка
            if (bull_count_in_seq != bull_count) or (cow_count_in_seq != cow_count):
                self.sequence_set.remove(seq)
