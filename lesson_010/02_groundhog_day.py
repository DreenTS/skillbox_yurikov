# -*- coding: utf-8 -*-

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.
import random


class IamGodError(Exception):

    def __str__(self):
        return 'Он возомнил себя Богом. Все его отвергли. Снова.'


class DrunkError(Exception):

    def __str__(self):
        return 'Он напился и его тело того не выдержало. Всё по-новой.'


class CarCrashError(Exception):

    def __str__(self):
        return 'Он разбился в автокатастрофе. В следующий раз повезёт.'


class GluttonyError(Exception):

    def __str__(self):
        return 'Он умер от переедания. Попробуем ещё раз.'


class DepressionError(Exception):

    def __str__(self):
        return 'Депрессия опасная штука. Ещё один шанс.'


class SuicideError(Exception):

    def __str__(self):
        return 'Он покончил с собой. Пусть попробует ещё разок.'


def one_day(choice_list):
    if random.randint(1, 13) == 13:
        exc = random.choice(choice_list)
        raise exc
    else:
        return random.randint(1, 7)


ENLIGHTENMENT_CARMA_LEVEL = 777

exc_list = [IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError]
curr_carma = 0
days = 0
while True:
    days += 1
    if curr_carma >= ENLIGHTENMENT_CARMA_LEVEL:
        break
    try:
        curr_carma += one_day(exc_list)
    except Exception as exc:
        with open('reloads.txt', 'a', encoding='utf8') as file:
            file.write(f'[День {days}. {exc}]\n')
print(f'Ура! carma = {curr_carma}, вышли из цикла на {days} день.')

# https://goo.gl/JnsDqu
