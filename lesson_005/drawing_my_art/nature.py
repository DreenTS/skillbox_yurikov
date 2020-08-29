# -*- coding: utf-8 -*-

import simple_draw as sd


def draw_ground():
    sd.rectangle(sd.get_point(0, 0), sd.get_point(1200, 45), color=(102, 51, 0), width=0)
    sd.rectangle(sd.get_point(0, 45), sd.get_point(1200, 73), color=(0, 204, 0), width=0)


def draw_tree(point, angle, length=75.0):
    color = (153, 76, 0)
    if length < 5:
        return
    if length < 25:
        color = (0, 204, 0)
    v1 = sd.get_vector(start_point=point, angle=angle, length=length)
    v1.draw(width=3, color=color)
    new_angle = sd.random_number(18, 43)
    new_length = sd.random_number(60, 91) / 100
    draw_tree(point=v1.end_point, angle=angle + new_angle, length=length * new_length)
    draw_tree(point=v1.end_point, angle=angle - new_angle, length=length * new_length)


def draw_rainbow():
    rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                      sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)
    radius = 970
    for color in rainbow_colors:
        center_point = sd.get_point(420, 0)
        sd.circle(center_point, radius, color, 20)
        radius -= 20


def draw_cloud():
    cloud_color = sd.COLOR_WHITE
    cloud_circle_color = sd.COLOR_CYAN
    for x in range(140, 201, 20):
        sd.circle(sd.get_point(x, 400), 20, width=0, color=cloud_color)
        sd.circle(sd.get_point(x, 400), 20, width=4, color=cloud_circle_color)
    for x in range(120, 221, 20):
        sd.circle(sd.get_point(x, 380), 20, width=0, color=cloud_color)
        sd.circle(sd.get_point(x, 380), 20, width=4, color=cloud_circle_color)
    for x in range(140, 201, 20):
        sd.circle(sd.get_point(x, 360), 20, width=0, color=cloud_color)
        sd.circle(sd.get_point(x, 360), 20, width=4, color=cloud_circle_color)


def draw_sun():
    center_point = sd.get_point(150, 570)
    sd.circle(center_point, 60, width=0)
    list_of_shines = []
    shine_point = sd.get_point(150, 570)
    for shine in range(0, 361, 45):
        list_of_shines.append(sd.get_vector(start_point=shine_point, angle=shine, length=110))
        list_of_shines.append(sd.get_vector(start_point=shine_point, angle=shine + 22.5, length=80))
    for shine in list_of_shines:
        shine.draw(width=2)


def draw_snow():
    dict_of_snow = {}
    for i in range(25):
        random_point = sd.get_point(sd.random_number(120, 200), sd.random_number(320, 325))
        random_length = sd.random_number(10, 15)
        dict_of_snow[i] = {'start_point': random_point, 'length': random_length}
    while True:
        sd.start_drawing()
        for index, snowflake_data in dict_of_snow.items():
            point_for_snowflake = snowflake_data['start_point']
            if point_for_snowflake.y <= 80:
                snowflake_data['start_point'] = sd.get_point(sd.random_number(120, 200), sd.random_number(320, 325))
            else:
                sd.snowflake(center=point_for_snowflake, length=snowflake_data['length'], color=sd.background_color)
                point_for_snowflake.y -= sd.random_number(10, 30)
                point_for_snowflake.x -= sd.random_number(-10, 11)
                sd.snowflake(center=point_for_snowflake, length=snowflake_data['length'])
        sd.finish_drawing()
        sd.sleep(0.1)
        if sd.user_want_exit():
            break


def draw_nature():
    draw_ground()
    draw_rainbow()
    draw_cloud()
    draw_sun()
    draw_tree(sd.get_point(1000, 70), 90)
    draw_snow()

