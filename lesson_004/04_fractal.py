# -*- coding: utf-8 -*-

import simple_draw as sd

# 1) Написать функцию draw_branches, которая должна рисовать две ветви дерева из начальной точки
# Функция должна принимать параметры:
# - точка начала рисования,
# - угол рисования,
# - длина ветвей,
# Отклонение ветвей от угла рисования принять 30 градусов,

# 2) Сделать draw_branches рекурсивной
# - добавить проверку на длину ветвей, если длина меньше 10 - не рисовать
# - вызывать саму себя 2 раза из точек-концов нарисованных ветвей,
#   с параметром "угол рисования" равным углу только что нарисованной ветви,
#   и параметром "длина ветвей" в 0.75 меньшей чем длина только что нарисованной ветви

# 3) Запустить вашу рекурсивную функцию, используя следующие параметры:
# root_point = sd.get_point(300, 30)
# draw_branches(start_point=root_point, angle=90, length=100)

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# Возможный результат решения см lesson_004/results/exercise_04_fractal_01.jpg

# можно поиграть -шрифтами- цветами и углами отклонения

'''
Основная часть
'''

# def draw_branches(point, angle, length=50.0):
#     if length < 10:
#         return
#     v1 = sd.get_vector(start_point=point, angle=angle, length=length)
#     v1.draw(width=2)
#     draw_branches(point=v1.end_point, angle=angle + 30, length=length * .75)
#     draw_branches(point=v1.end_point, angle=angle - 30, length=length * .75)
#
#
# start_point = sd.get_point(300, 30)
# draw_branches(point=start_point, angle=90, length=100)


# 4) Усложненное задание (делать по желанию)
# - сделать рандомное отклонение угла ветвей в пределах 40% от 30-ти градусов
# - сделать рандомное отклонение длины ветвей в пределах 20% от коэффициента 0.75
# Возможный результат решения см lesson_004/results/exercise_04_fractal_02.jpg

# Пригодятся функции
# sd.random_number()
'''
Дополнительная часть
'''


def draw_branches(point, angle, length=50.0):
    if length < 5:
        return
    v1 = sd.get_vector(start_point=point, angle=angle, length=length)
    v1.draw(width=2)
    new_angle = sd.random_number(18, 43)
    new_length = sd.random_number(60, 91) / 100
    draw_branches(point=v1.end_point, angle=angle + new_angle, length=length * new_length)
    draw_branches(point=v1.end_point, angle=angle - new_angle, length=length * new_length)


start_point = sd.get_point(300, 30)
draw_branches(point=start_point, angle=90, length=100)

sd.pause()

# зачёт!
