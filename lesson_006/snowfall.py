import simple_draw as sd

DICT_OF_SNOW = {}
LAST_SNOWFLAKE = -1


def create_snowflakes(n):
    global LAST_SNOWFLAKE
    for _ in range(n):
        LAST_SNOWFLAKE += 1
        random_point = sd.get_point(sd.random_number(0, 801), sd.random_number(850, 1600))
        random_length = sd.random_number(10, 101)
        DICT_OF_SNOW[LAST_SNOWFLAKE] = {'start_point': random_point, 'length': random_length}


def draw_snowflakes_with_color(color):
    sd.start_drawing()
    for index, snowflake_data in DICT_OF_SNOW.items():
        point_for_snowflake = snowflake_data['start_point']
        sd.snowflake(center=point_for_snowflake, length=snowflake_data['length'], color=color)
    sd.finish_drawing()


def next_step_snowflakes():
    for temp, point_for_snowflake in DICT_OF_SNOW.items():
        point_for_snowflake['start_point'].y -= sd.random_number(10, 100)
        point_for_snowflake['start_point'].x -= sd.random_number(-10, 15)


def numbers_bottom_screen():
    delete_list = []
    for index, snowflake_data in DICT_OF_SNOW.items():
        point_for_snowflake = snowflake_data['start_point']
        if point_for_snowflake.y <= 25:
            delete_list.append(index)
    return delete_list


def delete_snowflakes(numbers):
    for snowflake in numbers:
        del DICT_OF_SNOW[snowflake]

