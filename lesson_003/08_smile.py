# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw as sd
from random import uniform

sd.resolution = (1200, 600)

# Написать функцию отрисовки смайлика по заданным координатам
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.


def draw_smile(x, y, colors):
    # Определение множителя для масштбирования всего смайла
    multiplier = uniform(0.5, 1.25)

    # Отрисовка лица
    radius = 75 * multiplier
    face_point = sd.get_point(x, y)
    sd.circle(face_point, radius, colors, 0)
    sd.circle(face_point, radius, (0, 0, 0), 2)

    # Отрисовка глаз
    sd.line(sd.get_point(x - 48 * multiplier, y + 10 * multiplier),
            sd.get_point(x - 33 * multiplier, y + 40 * multiplier), (0, 0, 0), 4)
    sd.line(sd.get_point(x - 33 * multiplier, y + 40 * multiplier),
            sd.get_point(x - 18 * multiplier, y + 10 * multiplier), (0, 0, 0), 4)
    sd.line(sd.get_point(x + 12 * multiplier, y + 10 * multiplier),
            sd.get_point(x + 27 * multiplier, y + 40 * multiplier), (0, 0, 0), 4)
    sd.line(sd.get_point(x + 27 * multiplier, y + 40 * multiplier),
            sd.get_point(x + 43 * multiplier, y + 10 * multiplier), (0, 0, 0), 4)

    # Отрисовка рта
    sd.ellipse(sd.get_point(x - 45 * multiplier, y - 50 * multiplier),
               sd.get_point(x + 45 * multiplier, y - 10 * multiplier), (255, 20, 147), 0)
    sd.ellipse(sd.get_point(x - 45 * multiplier, y - 50 * multiplier),
               sd.get_point(x + 45 * multiplier, y - 10 * multiplier), (0, 0, 0), 4)


for _ in range(10):
    point_x = sd.random_number(20, 1180)
    point_y = sd.random_number(20, 580)
    color = sd.random_color()
    draw_smile(point_x, point_y, color)
sd.pause()
# зачет!