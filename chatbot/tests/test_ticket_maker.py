import unittest
from unittest.mock import patch

from ticket_maker import *


class TicketMakerTest(unittest.TestCase):

    def test_normal(self):
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
        template = cv2.imread('test_templates/response_image_template.png')
        raw_template_data = cv2.imencode('.png', template)[1].tobytes()

        with patch('ticket_maker.requests.get')as get:
            get.return_value.raw.read.return_value = raw_template_data
            ticket_maker = TicketMaker(data=data)
            ticket_maker.conf['template'] = 'test_templates/ticket_template.png'
            ticket = ticket_maker.draw()

        img = cv2.imread('test_templates/ticket_template_for_tests.png')
        res_bytes = cv2.imencode('.png', img)[1].tobytes()
        res_bytesio = BytesIO(res_bytes)

        self.assertEqual(ticket.read(), res_bytesio.read())


if __name__ == '__main__':
    unittest.main()
