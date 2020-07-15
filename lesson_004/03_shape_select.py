# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (800, 800)
# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg


def paint_fuction(point, angle, length=100, color=sd.COLOR_YELLOW):
    new_point = point
    for angles in range(0, 360, angle):
        if angles + angle >= 360:
            sd.line(start_point=new_point, end_point=point, width=3, color=color)
        else:
            vector = sd.get_vector(start_point=new_point, angle=angles, length=length)
            vector.draw(color=color, width=3)
            new_point = vector.end_point


def triangle(point, angle, length=100, color=sd.COLOR_YELLOW):
    paint_fuction(point, angle, length, color)


def square(point, angle, length=100, color=sd.COLOR_YELLOW):
    paint_fuction(point, angle, length, color)


def pentagon(point, angle, length=100, color=sd.COLOR_YELLOW):
    paint_fuction(point, angle, length, color)


def hexagon(point, angle, length=100, color=sd.COLOR_YELLOW):
    paint_fuction(point, angle, length, color)


print('\nВыберите фигуру, которая будет отрисована:')
figures = ['Треугольник', 'Квадрат', 'Пятиугольник', 'Шестиугольник']
for index, items in enumerate(figures):
    print(f'{index + 1} : {items}')
while True:
    main_figure = int(input('Выберите номер желаемой фигуры: '))
    if 0 < main_figure <= len(figures):
        break
    else:
        print('Номер фигуры некорректный!')
if main_figure == 1:
    point_0 = sd.get_point(325, 325)
    triangle(point=point_0, angle=120, length=150)
elif main_figure == 2:
    point_0 = sd.get_point(325, 325)
    square(point=point_0, angle=90, length=150)
elif main_figure == 3:
    point_0 = sd.get_point(325, 325)
    pentagon(point=point_0, angle=72, length=150)
elif main_figure == 4:
    point_0 = sd.get_point(325, 325)
    hexagon(point=point_0, angle=60, length=150)
sd.pause()
