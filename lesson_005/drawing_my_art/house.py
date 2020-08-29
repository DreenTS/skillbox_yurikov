# -*- coding: utf-8 -*-

import simple_draw as sd


def draw_wall():
    sd.rectangle(sd.get_point(350, 70), sd.get_point(800, 370), color=(139, 69, 19))
    color = sd.COLOR_YELLOW
    for y in range(70, 370, 25):
        if y % 2 == 0:
            for x in range(350, 800, 50):
                brick_left_point = sd.get_point(x, y)
                brick_right_point = sd.get_point(x + 50, y + 25)
                sd.rectangle(brick_left_point, brick_right_point, color, 1)
        else:
            brick_left_point = sd.get_point(350, y)
            brick_right_point = sd.get_point(375, y + 25)
            sd.rectangle(brick_left_point, brick_right_point, color, 1)
            for x in range(375, 750, 50):
                brick_left_point = sd.get_point(x, y)
                brick_right_point = sd.get_point(x + 50, y + 25)
                sd.rectangle(brick_left_point, brick_right_point, color, 1)
                x += 50
            brick_left_point = sd.get_point(775, y)
            brick_right_point = sd.get_point(800, y + 25)
            sd.rectangle(brick_left_point, brick_right_point, color, 1)


def draw_window():
    sd.rectangle(sd.get_point(450, 145), sd.get_point(700, 322), color=(102, 178, 255))
    sd.rectangle(sd.get_point(450, 145), sd.get_point(700, 322), color=sd.COLOR_BLACK, width=5)
    sd.line(sd.get_point(575, 145), sd.get_point(575, 322), color=sd.COLOR_BLACK, width=5)
    sd.line(sd.get_point(450, 235), sd.get_point(700, 235), color=sd.COLOR_BLACK, width=5)


def draw_roof():
    sd.polygon([sd.get_point(320, 370), sd.get_point(575, 550), sd.get_point(825, 370), sd.get_point(320, 370)],
               color=(204, 0, 0), width=0)


def draw_house():
    draw_wall()
    draw_window()
    draw_roof()

