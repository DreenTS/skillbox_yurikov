from io import BytesIO

import numpy as np
import requests
import cv2

import settings


class TicketMaker:
    """
    Класс для создания изображений регистрацией билетя.

    """

    def __init__(self, data):
        self.conf = settings.TICKET_CONFIG
        self.data = {
            'photo': data.photo,
            'name': data.name,
            'departure_city': data.context['departure_city'],
            'arrival_city': data.context['arrival_city'],
            'number_of_seats': data.context['number_of_seats'],
            'phone_number': data.context['phone_number'],
            'date': data.context['date'],
            'price': data.context['price'],
        }

    def draw(self):
        """
        Запуск отрисовки.

        Получает аватар пользователя из сети.
        Вызывает дополнительные методы _add_photo() и _print_text()
        (подробнее см. в docstrings методов).
        Формирует bytes-строку изображения и возвращает BytesIO object, созданный из данной строки.

        :return: BytesIO object, изображение в представлении BytesIO object
        """
        response = requests.get(self.data['photo'], stream=True).raw
        img_bytes = np.asarray(bytearray(response.read()), dtype="uint8")
        user_photo = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

        res = cv2.imread(self.conf['template'])
        resized = cv2.resize(user_photo, (200, 200), interpolation=cv2.INTER_AREA)
        self._add_photo(src=res, photo=resized)
        self._print_text(src=res)
        res_bytes = cv2.imencode('.png', res)[1].tobytes()
        res_bytesio = BytesIO(res_bytes)
        return res_bytesio

    def _add_photo(self, src, photo):
        """
        Добавление аватара на билет.

        :param src: np.ndarray, массив данных билета
        :param photo: np.ndarray, массив данных аватара пользователя
        :return: None
        """

        dx = round(src.shape[1] * .96) - 200
        dy = round(src.shape[0] * .24)
        for y, x_line in enumerate(photo):
            for x, color in enumerate(x_line):
                src[dy + y][dx + x] = color

    def _print_text(self, src):
        """
        Печать текста на билете.

        :param src: np.ndarray, массив данных билета
        :return: None
        """

        for k, v in self.data.items():
            if k in self.conf.keys():
                x = round(src.shape[1] * self.conf[k][0])
                y = round(src.shape[0] * self.conf[k][1])
                cv2.putText(src, v, (x, y), cv2.FONT_HERSHEY_COMPLEX, .55, (0, 0, 0))


if __name__ == '__main__':
    data = {
        'photo': 'https://vk.com/images/camera_200.png',
        'name': 'Василий Юриков',
        'date': '07-10-2021 14:05',
        'price': '18 500 рублей',
        'comment': '1',
        'arrival_city': 'Владивосток',
        'departure_city': 'Токио',
        'number_of_seats': '1',
        'phone_number': '+79999999999'
    }
    image_maker = TicketMaker(data=data)
    ticket = image_maker.draw()
