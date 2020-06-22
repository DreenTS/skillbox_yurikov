# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw as sd

sd.resolution = (1200, 600)
# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for

color = (139, 69, 19)
for y in range(0, 601, 50):
    brick_y = y
    if (y / 50) % 2 == 0:
        brick_x = 0
    else:
        brick_x = -50
    for x in range(0, 1201, 100):
        brick_left_point = sd.get_point(brick_x, brick_y)
        brick_right_point = sd.get_point(brick_x + 100, brick_y + 50)
        sd.rectangle(brick_left_point, brick_right_point, color, 1)
        brick_x += 100

# Подсказки:
#  Для отрисовки кирпича использовать функцию rectangle
#  Алгоритм должен получиться приблизительно такой:
#
#   цикл по координате Y
#       вычисляем сдвиг ряда кирпичей
#       цикл координате X
#           вычисляем правый нижний и левый верхний углы кирпича
#           рисуем кирпич

sd.pause()
# зачет!