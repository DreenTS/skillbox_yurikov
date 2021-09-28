import unittest
import random
from copy import deepcopy

from pony.orm import rollback
from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot
from settings import *
from unittest.mock import Mock, patch


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        test_func(*args, **kwargs)
        rollback()
    return wrapper


class BotTest(unittest.TestCase):

    RAW_EVENT = {
        'type': 'message_new',
        'object': {
            'message': {
                'date': 1630987867, 'from_id': 134431423, 'id': 144, 'out': 0, 'peer_id': 134431423,
                'text': 'Привет', 'conversation_message_id': 141, 'fwd_messages': [], 'important': False,
                'random_id': 0,
                'attachments': [], 'is_hidden': False
            },
            'client_info': {
                'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link',
                                   'callback', 'intent_subscribe', 'intent_unsubscribe'],
                'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0
            }
        },
        'group_id': 200346432, 'event_id': 'd2a0a1ea65f91dbba501152daf09307c3d507011'
    }

    INPUTS = [
        'Привет',
        '/help',
        '/ticket',
        'Вашингтон',
        'Токио',
        '30-10-2021',
        '1',
        '6',
        '5',
        'My comment.',
        'Да',
        '+79991002030',
    ]

    EXPECTED_OUTPUTS = [
        DEFAULT_ANSWERS[0],
        INTENTS[0]['answer'],
        SCENARIOS['ticket_order']['steps']['1_departure_city_indication']['text'],
        SCENARIOS['ticket_order']['steps']['2_arrival_city_indication']['text'],
        SCENARIOS['ticket_order']['steps']['3_date_input']['text'],
        '1)\n....Дата: {}\n....Стоимость билета: {}\n\n'.format(*FLIGHTS['вашингтон']['токио'][0].values()) +
        SCENARIOS['ticket_order']['steps']['4_flight_selection']['text'],
        SCENARIOS['ticket_order']['steps']['5_number_of_seats_indication']['text'],
        SCENARIOS['ticket_order']['steps']['5_number_of_seats_indication']['failure_text'],
        SCENARIOS['ticket_order']['steps']['6_comment']['text'],
        'Проверка данных авиабилета (стоимость билета указана за одно место):\n....'
        'Откуда: Вашингтон\n....'
        'Куда: Токио\n....'
        'Дата: 30-10-2021 16:20\n....Стоимость билета: 27 800 рублей\n....'
        'Количество мест: 5\n....'
        'Комментарий: My comment.\n\n' +
        SCENARIOS['ticket_order']['steps']['7_data_checking']['text'],
        SCENARIOS['ticket_order']['steps']['8_phone_number_request']['text'],
        SCENARIOS['ticket_order']['steps']['9_say_goodbye']['text'],
    ]

    def test_run(self):
        count = 5
        obj = int
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_mock_listen_mock = Mock()
        long_poller_mock_listen_mock.listen = long_poller_mock
        logger_mock = Mock()
        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_mock_listen_mock):
                bot = Bot('group_id', 'token', logger_mock)
                bot.on_event = Mock()
                bot.create_and_send_ticket = Mock()
                bot.run()
                bot.on_event.assert_called()
                bot.on_event.assert_called_with(obj)
                result = bot.on_event.call_count
                self.assertEqual(result, count)

    @isolate_db
    def test_on_event(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock
        random.choice = Mock(return_value=DEFAULT_ANSWERS[0])

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock(return_value=events)
        long_poller_mock_listen_mock = Mock()
        long_poller_mock_listen_mock.listen = long_poller_mock
        logger_mock = Mock()

        full_name = [
            {
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'photo_max': 'https://vk.com/images/camera_200.png'
            }
        ]
        vk_api_method_mock = Mock(return_value=full_name)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock_listen_mock):
            bot = Bot('group_id', 'token', logger_mock)
            bot.api = api_mock
            bot.vk.method = vk_api_method_mock
            bot.create_and_send_ticket = Mock()
            for event in events:
                bot.on_event(event)
        self.assertEqual(send_mock.call_count, len(self.INPUTS))

        real_outputs = []
        for call in send_mock.call_args_list:
            agrs, kwargs = call
            real_outputs.append(kwargs['message'])
        self.assertEqual(real_outputs, self.EXPECTED_OUTPUTS)


if __name__ == '__main__':
    unittest.main()
