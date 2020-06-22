# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (1200, 600)

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
point_1 = sd.get_point(300, 400)
radius = 95
for _ in range(3):
    radius += 5
    sd.circle(point_1, radius)


# Написать функцию рисования пузырька, принммающую 3 (или более) параметра: точка рисования, шаг и цвет
def draw_bubble(x, y, step, circle_color, circle_width):
    # Рисует пузырёк с центром в точке (x, y),
    # шагом step, цветом color, случайного радиуса, толщиной width
    circle_center = sd.get_point(x, y)
    circle_radius = sd.random_number(50, 200)
    for _ in range(3):
        circle_radius += step
        sd.circle(circle_center, circle_radius, circle_color, circle_width)


draw_bubble(400, 250, 8, (255, 0, 0), 3)

# Нарисовать 10 пузырьков в ряд
for i in range(100, 1001, 100):
    sd.circle(sd.get_point(i, 100), 35)
    sd.circle(sd.get_point(i, 100), 40)
    sd.circle(sd.get_point(i, 100), 45)

# Нарисовать три ряда по 10 пузырьков
for i in range(100, 301, 100):
    for j in range(100, 1001, 100):
        sd.circle(sd.get_point(j, i), 35)
        sd.circle(sd.get_point(j, i), 40)
        sd.circle(sd.get_point(j, i), 45)

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
for _ in range(100):
    radius = sd.random_number(50, 100)
    radius_step = sd.random_number(4, 8)
    width = sd.random_number(1, 3)
    random_center = sd.random_point()
    random_color = sd.random_color()
    for _ in range(3):
        radius += radius_step
        sd.circle(random_center, radius, random_color)

sd.pause()

# зачет!
