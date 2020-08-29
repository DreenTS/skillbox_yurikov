# -*- coding: utf-8 -*-

import simple_draw as sd


def draw_smile():
    # Отрисовка лица
    x = 637.5
    y = 189.25
    face_point = sd.get_point(x, y)
    sd.circle(face_point, 75 * 0.53, sd.COLOR_YELLOW, 0)
    sd.circle(face_point, 75 * 0.53, (0, 0, 0), 2)

    # Отрисовка глаз
    sd.line(sd.get_point(x - 48 * 0.53, y + 10 * 0.53),
            sd.get_point(x - 33 * 0.53, y + 40 * 0.53), (0, 0, 0), 4)
    sd.line(sd.get_point(x - 33 * 0.53, y + 40 * 0.53),
            sd.get_point(x - 18 * 0.53, y + 10 * 0.53), (0, 0, 0), 4)
    sd.line(sd.get_point(x + 12 * 0.53, y + 10 * 0.53),
            sd.get_point(x + 27 * 0.53, y + 40 * 0.53), (0, 0, 0), 4)
    sd.line(sd.get_point(x + 27 * 0.53, y + 40 * 0.53),
            sd.get_point(x + 43 * 0.53, y + 10 * 0.53), (0, 0, 0), 4)

    # Отрисовка рта
    sd.ellipse(sd.get_point(x - 45 * 0.53, y - 50 * 0.53),
               sd.get_point(x + 45 * 0.53, y - 10 * 0.53), (255, 20, 147), 0)
    sd.ellipse(sd.get_point(x - 45 * 0.53, y - 50 * 0.53),
               sd.get_point(x + 45 * 0.53, y - 10 * 0.53), (0, 0, 0), 4)
