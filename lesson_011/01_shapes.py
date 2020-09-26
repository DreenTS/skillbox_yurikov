# -*- coding: utf-8 -*-

import simple_draw as sd

# На основе вашего кода из решения lesson_004/01_shapes.py сделать функцию-фабрику,
# которая возвращает функции рисования треугольника, четырехугольника, пятиугольника и т.д.
#
# Функция рисования должна принимать параметры
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Функция-фабрика должна принимать параметр n - количество сторон.

sd.resolution = (800, 800)


def get_polygon(n):

    def draw_func(point, angle, length):
        new_angle = angle
        new_point = point
        for side in range(n):
            if new_angle + 360 / n >= 360:
                sd.line(start_point=new_point, end_point=point, width=3)
            else:
                vector = sd.get_vector(start_point=new_point, angle=new_angle, length=length)
                vector.draw(width=3)
                new_point = vector.end_point
                new_angle += 360 / n

    return draw_func


draw_triangle = get_polygon(n=3)
draw_triangle(point=sd.get_point(150, 100), angle=13, length=150)
draw_square = get_polygon(n=4)
draw_square(point=sd.get_point(450, 100), angle=26, length=150)
draw_pentagon = get_polygon(n=5)
draw_pentagon(point=sd.get_point(150, 300), angle=35, length=150)
draw_hexagon = get_polygon(n=6)
draw_hexagon(point=sd.get_point(450, 300), angle=41, length=150)


sd.pause()
# зачет!