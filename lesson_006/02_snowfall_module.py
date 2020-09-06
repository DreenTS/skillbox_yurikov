# -*- coding: utf-8 -*-

import simple_draw as sd
import snowfall

# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
# снежинки хранить в глобальных переменных модуля snowfall
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall
sd.resolution = (800, 800)
# создать_снежинки(N)
snowfall.create_snowflakes(25)
while True:
    #  нарисовать_снежинки_цветом(color=sd.background_color)
    snowfall.draw_snowflakes_with_color(color=sd.background_color)
    #  сдвинуть_снежинки()
    snowfall.next_step_snowflakes()
    #  нарисовать_снежинки_цветом(color)
    snowfall.draw_snowflakes_with_color(color=sd.COLOR_WHITE)
    #  если есть номера_достигших_низа_экрана() то
    #       удалить_снежинки(номера)
    #       создать_снежинки(count)
    dead_snowflakes = snowfall.numbers_bottom_screen()
    if len(dead_snowflakes) > 0:
        snowfall.delete_snowflakes(dead_snowflakes)
        snowfall.create_snowflakes(len(dead_snowflakes))
        dead_snowflakes.clear()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
