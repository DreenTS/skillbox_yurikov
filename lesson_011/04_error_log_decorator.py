# -*- coding: utf-8 -*-

# Написать декоратор, который будет логировать (записывать в лог файл)
# ошибки из декорируемой функции и выбрасывать их дальше.
#
# Имя файла лога - function_errors.log
# Формат лога: <имя функции> <параметры вызова> <тип ошибки> <текст ошибки>
# Лог файл открывать каждый раз при ошибке в режиме 'a'

# Усложненное задание (делать по желанию).
# Написать декоратор с параметром - именем файла
#
# @log_errors('function_errors.log')
# def func():
#     pass

from pprint import pprint


def log_errors_with_file(file_name):
    def log_errors(func):

        def surrogate(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except ValueError as exc:
                with open(file_name, 'a', encoding='utf8') as file:
                    file.write(f'[{func}: {args, kwargs}. ValueError: {exc}]\n')
                raise ValueError(f'{func}: {args, kwargs}. ValueError: {exc}')
            except ZeroDivisionError as exc:
                with open(file_name, 'a', encoding='utf8') as file:
                    file.write(f'[{func}: {args, kwargs}. ZeroDivisionError: {exc}]\n')
                raise ZeroDivisionError(f'{func}: {args, kwargs}. ZeroDivisionError: {exc}')
            return result

        return surrogate
    return log_errors


# Проверить работу на следующих функциях
@log_errors_with_file(file_name='function_errors.log')
def perky(*args):
    return args[0] / 0


@log_errors_with_file(file_name='function_errors.log')
def check_line(*args):
    name, email, age = str(args[0]).split(' ')
    if not name.isalpha():
        raise ValueError("it's not a name")
    if '@' not in email or '.' not in email:
        raise ValueError("it's not an email")
    if not 10 <= int(age) <= 99:
        raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]
ok_list = []

for line in lines:
    try:
        check_line(line)
        ok_list.append(line)
    except Exception as exc:
        print(f'[Error: {exc}]')
print('OK for:')
pprint(ok_list)

try:
    perky(42)
except Exception as exc:
    print(f'[Error: {exc}]')

# зачет! 