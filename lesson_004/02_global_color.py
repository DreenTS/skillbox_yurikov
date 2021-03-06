# -*- coding: utf-8 -*-
import simple_draw as sd


# Добавить цвет в функции рисования геом. фигур. из упр lesson_004/01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих:
#   вывести список всех цветов с номерами и ждать ввода номера желаемого цвета.
# Потом нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см lesson_004/results/exercise_02_global_color.jpg


def paint_function(point, angle, length=100, color=sd.COLOR_YELLOW):
    new_point = point
    for angles in range(0, 360, angle):
        if angles + angle >= 360:
            sd.line(start_point=new_point, end_point=point, width=3, color=color)
        else:
            vector = sd.get_vector(start_point=new_point, angle=angles, length=length)
            vector.draw(color=color, width=3)
            new_point = vector.end_point


def triangle(point, length=100, color=sd.COLOR_YELLOW):
    paint_function(point=point, angle=120, length=length, color=color)


def square(point, length=100, color=sd.COLOR_YELLOW):
    paint_function(point=point, angle=90, length=length, color=color)


def pentagon(point, length=100, color=sd.COLOR_YELLOW):
    paint_function(point=point, angle=72, length=length, color=color)


def hexagon(point, length=100, color=sd.COLOR_YELLOW):
    paint_function(point=point, angle=60, length=length, color=color)


print('\nВыберите цвет, которым будут отрисованы все фигуры:')
colors = {
    '1': ['БЕЛЫЙ', sd.COLOR_WHITE],
    '2': ['ЧЁРНЫЙ', sd.COLOR_BLACK],
    '3': ['КРАСНЫЙ', sd.COLOR_RED],
    '4': ['ОРАНЖЕВЫЙ', sd.COLOR_ORANGE],
    '5': ['ЖЁЛТЫЙ', sd.COLOR_YELLOW],
    '6': ['ЗЕЛЁНЫЙ', sd.COLOR_GREEN],
    '7': ['СИНИЙ', sd.COLOR_CYAN],
    '8': ['ГОЛУБОЙ', sd.COLOR_BLUE],
    '9': ['ФИОЛЕТОВЫЙ', sd.COLOR_PURPLE]
}

for items in colors:
    print(f'{items} : {colors[items][0]}')

while True:
    main_color = input('Выберите номер желаемого цвета: ')
    if main_color in colors:
        break
    else:
        print('Номер цвета некорректный!')

point_for_triangle = sd.get_point(50, 100)
triangle(point=point_for_triangle, length=150, color=colors[main_color][1])
point_for_square = sd.get_point(350, 100)
square(point=point_for_square, length=150, color=colors[main_color][1])
point_for_pentagon = sd.get_point(50, 300)
pentagon(point=point_for_pentagon, length=150, color=colors[main_color][1])
point_for_hexagon = sd.get_point(350, 300)
hexagon(point=point_for_hexagon, length=150, color=colors[main_color][1])

sd.pause()

# зачёт!
