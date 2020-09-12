# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())
from random import choice


class Water:

    def __init__(self):
        self.name = 'Вода'

    def __add__(self, other):
        if other.name == 'Воздух':  # TODO: принадлежность объекта к классу лучше определять через isinstance
            return Storm()
        elif other.name == 'Огонь':
            return Steam()
        elif other.name == 'Земля':
            return Dirt()
        else:
            return None

    def __str__(self):
        return self.name


class Air:
    def __init__(self):
        self.name = 'Воздух'

    def __add__(self, other):
        if other.name == 'Вода':
            return Storm()
        elif other.name == 'Огонь':
            return Lightning()
        elif other.name == 'Земля':
            return Dust()
        else:
            return None

    def __str__(self):
        return self.name


class Fire:
    def __init__(self):
        self.name = 'Огонь'

    def __add__(self, other):
        if other.name == 'Вода':
            return Steam()
        elif other.name == 'Воздух':
            return Lightning()
        elif other.name == 'Земля':
            return Lava()
        else:
            return None

    def __str__(self):
        return self.name


class Earth:
    def __init__(self):
        self.name = 'Земля'

    def __add__(self, other):
        if other.name == 'Вода':
            return Dirt()
        elif other.name == 'Воздух':
            return Dust()
        elif other.name == 'Огонь':
            return Lava()
        else:
            return None

    def __str__(self):
        return self.name


class Storm:

    def __init__(self):
        self.name = 'Шторм'

    def __str__(self):
        return self.name


class Steam:

    def __init__(self):
        self.name = 'Пар'

    def __str__(self):
        return self.name


class Dirt:

    def __init__(self):
        self.name = 'Грязь'

    def __str__(self):
        return self.name


class Lightning:

    def __init__(self):
        self.name = 'Молния'

    def __str__(self):
        return self.name


class Dust:

    def __init__(self):
        self.name = 'Пыль'

    def __str__(self):
        return self.name


class Lava:

    def __init__(self):
        self.name = 'Лава'

    def __str__(self):
        return self.name


'''Усложнённое задание'''


class ReverseMagicConverter:

    """
        Обратный преобразователь взаимодействует только с производными
        от простых элементов и возвращает случайный из двух элементов
    """

    def __init__(self):
        self.name = 'Обратный преобразователь'

    def __add__(self, other):
        if other.name == 'Шторм':
            return choice([Water(), Air()])
        elif other.name == 'Пар':
            return choice([Water(), Fire()])
        elif other.name == 'Грязь':
            return choice([Water(), Earth()])
        elif other.name == 'Молния':
            return choice([Air(), Fire()])
        elif other.name == 'Пыль':
            return choice([Air(), Earth()])
        elif other.name == 'Лава':
            return choice([Fire(), Earth()])
        else:
            return None

    def __str__(self):
        return self.name


print(Water(), '+', Air(), '=', Water() + Air())
print(Water(), '+', Fire(), '=', Water() + Fire())
print(Water(), '+', Earth(), '=', Water() + Earth())
print(Air(), '+', Fire(), '=', Air() + Fire())
print(Air(), '+', Earth(), '=', Air() + Earth())
print(Fire(), '+', Earth(), '=', Fire() + Earth())
print(Fire(), '+', Dust(), '=', Fire() + Dust())

print('\nУсложнённое задание.')

print(ReverseMagicConverter(), '+', Storm(), '=', ReverseMagicConverter() + Storm())
print(ReverseMagicConverter(), '+', Steam(), '=', ReverseMagicConverter() + Steam())
print(ReverseMagicConverter(), '+', Dirt(), '=', ReverseMagicConverter() + Dirt())
print(ReverseMagicConverter(), '+', Lightning(), '=', ReverseMagicConverter() + Lightning())
print(ReverseMagicConverter(), '+', Dust(), '=', ReverseMagicConverter() + Dust())
print(ReverseMagicConverter(), '+', Lava(), '=', ReverseMagicConverter() + Lava())
print(ReverseMagicConverter(), '+', Fire(), '=', ReverseMagicConverter() + Fire())

# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.
