# Приветственное сообщение
start_text = 'Привет! Я - бот, с которым вы сможете поиграть в популярную логическую игру "Быки и коровы".\n' \
             '\n' \
             'Вот какие команды я знаю:\n' \
             '\n' \
             '/help - Вывести справочную информацию обо мне\n' \
             '/rules - Узнать правила игры\n' \
             '/user_play - Я загадываю, вы отгадываете\n' \
             '/bot_play - Вы загадываете, я отгадываю'

# Сообщение со справочной информацией
help_text = 'Хотите узнать о моём функционале?\n' \
            'Вот какие команды я знаю:\n' \
            '\n' \
            '/help - Вывести справочную информацию обо мне\n' \
            '/rules - Узнать правила игры\n' \
            '/user_play - Я загадываю, вы отгадываете\n' \
            '/bot_play - Вы загадываете, я отгадываю'

# Сообщение с правилами игры
rules_text = '"Быки и коровы" - это логическая игра, в которую играют два игрока. ' \
             'Один игрок загадывает четырёхзначную последовательность из неповторяющихся цифр ' \
             '(например, "0357" или "1759"), в то время как задача второго её отгадать за как можно меньшее ' \
             'количество попыток. Для этого отгадывающий игрок предлагает свои варианты данной последовательности ' \
             '(варианты также должны представлять из себя последовательность из четырёх неповторяющихся цифр), ' \
             'для каждого из которых загадавший игрок должен сказать, сколько "быков" и сколько "коров" было угадано. ' \
             'Количество "быков" показывает, сколько цифр были правильно угаданы и помещены на правильную позицию. ' \
             'Количество "коров" показывает, сколько цифр были правильно угаданы, ' \
             'но помещены на неправильную позицию. ' \
             'Чтобы выиграть, игроку требуется угадать всех четырёх быков, ' \
             'то есть указать правильную числовую последовательность.\n' \
             '\n' \
             'Чтобы узнать о моём функционале, введите команду /help.'

# Сообщение о некорректном вводе
incorrect_input_text = 'Извините, но я не понимаю, что вы написали. Попробуйте ввести /help, чтобы лучше ознакомиться ' \
                       'с моим функционалом.'

# Стартовое сообщение для userPlay-цикла
user_play_start_text = 'Отлично, давайте сыграем! Сейчас я загадаю последовательность из четырёх неповторяющихся ' \
                      'цифр (например, "0357" или "1759"), а ваша задача будет её отгадать. Для этого просто ' \
                      'введите свой вариант последовательности из четырёх неповторяющихся цифр, и я скажу, сколько ' \
                      '"быков" и "коров" вы угадали.\n' \
                      '\n' \
                      'Готовы? Начали! Можете смело вводить свой вариант.\n' \
                      '\n' \
                      '(Кстати, если вы вдруг захотите выйти из игры, то просто введите /stop вместо вашего варианта)'

# Приветственное сообщение для bot_play цикла
bot_play_start_text = 'Отлично, давайте сыграем! Загадайте последовательность из четырёх неповторяющихся цифр ' \
                     '(например, "0357" или "1759"), а я попробую её угадать. Для этого я буду отправлять вам свои ' \
                     'варианты, а вы должны написать сколько быков и коров я угадал. Чтобы сообщить мне эту ' \
                     'информацию, просто укажите два числа через пробел, первое из которых - количество быков, а ' \
                     'второе - количество коров (например, ввод "1 3" означает, что я угадал одного быка и ' \
                     'три коровы). Если мой вариант совпадёт с вашим, то просто введите "4 0" (четыре быка, ' \
                     'ноль коров). Будьте аккуратны, так как даже один неправильный ввод может привести ' \
                     'к тому, что я не смогу отгадать вашу последовательность.\n' \
                     '\n' \
                     'Готовы? Начали! Сейчас я отправлю вам свой первый вариант.\n' \
                     '\n' \
                     '(Кстати, если вы вдруг захотите выйти из игры, то просто введите /stop вместо вашего варианта)'

# Заключительное сообщение для user_play цикла
user_play_stop_text = 'Отлично поиграли! Станет скучно - обращайтесь ещё.\n' \
                     'Вот, кстати, какие команды я знаю:\n' \
                     '\n' \
                     '/help - Вывести справочную информацию обо мне\n' \
                     '/rules - Узнать правила игры\n' \
                     '/user_play - Я загадываю, вы отгадываете\n' \
                     '/bot_play - Вы загадываете, я отгадываю'

# Сообщение о том, сколько пользователь отгадал быков и коров
user_play_result_text = '{counter_user}) Быков - {bulls}, Коров - {cows}'

# Поздравление пользователя, угадавшего последовательность
user_play_win_text = 'Поздравляю! Вы угадали загаданную мною последовательность. ' \
                     'Это действительно "{sequence}".\n' \
                     '\n' \
                     'Количество затраченных попыток: {counter_user}'

# Сообщение о некорректно введённой последовательности
user_play_incorrect_input_text = 'Извините, но я не понимаю, что вы написали. Попробуйте ввести последовательность ' \
                                'из четырёх неповторяющихся чисел, чтобы продолжить игру, или команду /stop, чтобы ' \
                                'выйти из текущей игры.'

# Сообщение с вариантом последовательности от бота
bot_play_option_text = '{counter_bot}) Мой вариант: {last_bot_seq}'

# Заключительное сообщение для bot_play цикла
bot_play_stop_text = 'Отлично поиграли! Станет скучно - обращайтесь ещё.\n' \
                     'Вот, кстати, какие команды я знаю:\n' \
                     '\n' \
                     '/help - Вывести справочную информацию обо мне\n' \
                     '/rules - Узнать правила игры\n' \
                     '/user_play - Я загадываю, вы отгадываете\n' \
                     '/bot_play - Вы загадываете, я отгадываю'

# Сообщение о том, что бот правильно отгадал последовательность
bot_play_win_text = 'Ура, я угадал! Неужели это действительно была последовательность "{last_bot_seq}"?! ' \
                    'Какой же я молодец!\n' \
                    '\n' \
                    'Количество затраченных попыток: {counter_bot}'

# Сообщение о некорректно введённом количестве быков и коров
bot_play_incorrect_input_text = 'Извините, но я не понимаю, что вы написали. Попробуйте ввести количество ' \
                               'угаданных быков и коров через пробел (например, ввод "1 3" означает, что угаданы ' \
                               'один бык и три коровы), чтобы продолжить игру, или команду /stop, чтобы ' \
                               'выйти из текущей игры.'

# Сообщение о том, что у бота закончились варианты последовательностей
bot_play_empty_list_error_text = 'Извините, но у меня закончились варианты. Возможно, вы загадали некорректную ' \
                                'последовательность или ошиблись при подсчёте "быков" и "коров".'
