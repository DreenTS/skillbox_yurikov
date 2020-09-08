# -*- coding: utf-8 -*-

import simple_draw as sd

# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку
sd.resolution = (800, 800)


class Snowflake:

    def __init__(self):
        self.x = sd.random_number(0, 801)
        self.y = sd.random_number(850, 950)
        self.length = sd.random_number(10, 101)

    def __str__(self):
        return f'x = {self.x}, y = {self.y}, length = {self.length}'

    def clear_previous_picture(self):
        point = sd.get_point(self.x, self.y)
        sd.snowflake(center=point, length=self.length, color=sd.background_color)

    def move(self):
        self.x -= sd.random_number(-10, 15)
        self.y -= sd.random_number(10, 100)

    def draw(self):
        point = sd.get_point(self.x, self.y)
        sd.snowflake(center=point, length=self.length, color=sd.COLOR_WHITE)

    def can_fall(self):
        if self.y > 25:
            return True
        else:
            return False


def get_flakes(count):
    list_of_flakes = []
    for _ in range(count):
        list_of_flakes.append(Snowflake())
    return list_of_flakes


flake = Snowflake()

# while True:
#     flake.clear_previous_picture()
#     flake.move()
#     flake.draw()
#     if not flake.can_fall():
#         break
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break

# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:
flakes = get_flakes(count=35)  # создать список снежинок
while True:
    for flake in flakes:
        flake.clear_previous_picture()
        flake.move()
        flake.draw()
        if not flake.can_fall():
            flakes[flakes.index(flake)] = Snowflake()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
