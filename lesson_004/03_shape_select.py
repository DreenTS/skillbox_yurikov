# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (800, 800)
# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg


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


print('\nВыберите фигуру, которая будет отрисована:')
figure_dict = {
    '1': {
        'figure_name': 'Треугольник', 'function_name': triangle
    },
    '2': {
        'figure_name': 'Квадрат', 'function_name': square
    },
    '3': {
        'figure_name': 'Пятиугольник', 'function_name': pentagon
    },
    '4': {
        'figure_name': 'Шестиугольник', 'function_name': hexagon
    },
}

for index in figure_dict:
    print(f"{index} : {figure_dict[index]['figure_name']}")

while True:
    main_figure = input('Выберите номер желаемой фигуры: ')
    if 0 < int(main_figure) <= len(figure_dict):
        starting_point = sd.get_point(325, 325)
        paint_figure_func = figure_dict[main_figure]['function_name']
        paint_figure_func(point=starting_point, length=150)
        break
    else:
        print('Номер фигуры некорректный!')
sd.pause()
