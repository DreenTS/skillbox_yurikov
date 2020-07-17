# -*- coding: utf-8 -*-

import simple_draw as sd


# Часть 1.
# Написать функции рисования равносторонних геометрических фигур:
# - треугольника
# - квадрата
# - пятиугольника
# - шестиугольника
# Все функции должны принимать 3 параметра:
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Примерный алгоритм внутри функции:
#   # будем рисовать с помощью векторов, каждый следующий - из конечной точки предыдущего
#   текущая_точка = начальная точка
#   для угол_наклона из диапазона от 0 до 360 с шагом XXX
#      # XXX подбирается индивидуально для каждой фигуры
#      составляем вектор из текущая_точка заданной длины с наклоном в угол_наклона
#      рисуем вектор
#      текущая_точка = конечной точке вектора
#
# Использование копи-пасты - обязательно! Даже тем кто уже знает про её пагубность. Для тренировки.
# Как работает копипаста:
#   - одну функцию написали,
#   - копипастим её, меняем название, чуть подправляем код,
#   - копипастим её, меняем название, чуть подправляем код,
#   - и так далее.
# В итоге должен получиться ПОЧТИ одинаковый код в каждой функции

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# sd.line()
# Результат решения см lesson_004/results/exercise_01_shapes.jpg

# TODO, Василий, пожалуйста, обратите внимание, PyCharm подчёркивает слово fuction.
#  Дело в том, PyCharm есть проверка на корректность английских слов. Давайте исправим. в 01, 02 и 03 заданиях.

def paint_fuction(point, angle, length=100):
    new_point = point
    for angles in range(0, 360, angle):
        if angles + angle >= 360:
            sd.line(start_point=new_point, end_point=point, width=3)
        else:
            vector = sd.get_vector(start_point=new_point, angle=angles, length=length)
            vector.draw(width=3)
            new_point = vector.end_point


def triangle(point, angle, length=100):
    paint_fuction(point, angle, length)


def square(point, angle, length=100):
    paint_fuction(point, angle, length)


def pentagon(point, angle, length=100):
    paint_fuction(point, angle, length)


def hexagon(point, angle, length=100):
    paint_fuction(point, angle, length)


# TODO, Василий, пожалуйста, обратите внимание,
#  1. параметр angle лучше передавать в функцию paint_fuction().
#  И не оспользовать его в наших функциях triangle и т.д. Сейчас получается, что с помощью функции triangle
#  можно рисовать квадрат и т.д.
#  2. Одинаковые названия переменных лучше не использовать (point_0).

point_0 = sd.get_point(50, 100)
triangle(point=point_0, angle=120, length=150)
point_0 = sd.get_point(350, 100)
square(point=point_0, angle=90, length=150)
point_0 = sd.get_point(50, 300)
pentagon(point=point_0, angle=72, length=150)
point_0 = sd.get_point(350, 300)
hexagon(point=point_0, angle=60, length=150)

# Часть 1-бис.
# Попробуйте прикинуть обьем работы, если нужно будет внести изменения в этот код.
# Скажем, связывать точки не линиями, а дугами. Или двойными линиями. Или рисовать круги в угловых точках. Или...
# А если таких функций не 4, а 44? Код писать не нужно, просто представь объем работы... и запомни это.

# Часть 2 (делается после зачета первой части)
#
# Надо сформировать функцию, параметризированную в местах где была "небольшая правка".
# Это называется "Выделить общую часть алгоритма в отдельную функцию"
# Потом надо изменить функции рисования конкретных фигур - вызывать общую функцию вместо "почти" одинакового кода.
#
# В итоге должно получиться:
#   - одна общая функция со множеством параметров,
#   - все функции отрисовки треугольника/квадрата/етс берут 3 параметра и внутри себя ВЫЗЫВАЮТ общую функцию.
#
# Не забудте в этой общей функции придумать, как устранить разрыв в начальной/конечной точках рисуемой фигуры
# (если он есть. подсказка - на последней итерации можно использовать линию от первой точки)

# Часть 2-бис.
# А теперь - сколько надо работы что бы внести изменения в код? Выгода на лицо :)
# Поэтому среди программистов есть принцип D.R.Y. https://clck.ru/GEsA9
# Будьте ленивыми, не используйте копи-пасту!


sd.pause()
