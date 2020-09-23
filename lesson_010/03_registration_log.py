# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.

class NotNameError(Exception):

    def __str__(self):
        return 'NotNameError: the name field contains more than just letters'


class NotEmailError(Exception):

    def __str__(self):
        return 'NotEmailError: the email field does not contain @ or . (dot)'


def validation_method(one_line):
    if len(one_line) != 3:
        raise ValueError
    elif not one_line[0].isalpha():
        raise NotNameError
    elif '@' not in one_line[1] or '.' not in one_line[1]:
        raise NotEmailError
    elif int(one_line[2]) not in range(10, 100):
        raise ValueError


with open('registrations.txt', 'r', encoding='utf8') as file:
    for line in file:
        try:
            validation_method(line.split())
            with open('registrations_good.log', 'a', encoding='utf8') as good:
                good.write(line[:-1] + '\n')
        except ValueError as exc:
            with open('registrations_bad.log', 'a', encoding='utf8') as bad:
                bad.write(f'[Пользователь {line[:-1]}. Исключение ValueError: all three fields are not present, '
                          f'\nor the age field is not a number from 10 to 99.]\n')
        except NotNameError as exc:
            with open('registrations_bad.log', 'a', encoding='utf8') as bad:
                bad.write(f'[Пользователь {line[:-1]}. Исключение {exc}]\n')
        except NotEmailError as exc:
            with open('registrations_bad.log', 'a', encoding='utf8') as bad:
                bad.write(f'[Пользователь {line[:-1]}. Исключение {exc}]\n')
# зачет! 