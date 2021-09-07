import unittest
import random

from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot
from unittest.mock import Mock, patch, ANY


class BotTest(unittest.TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {
            'message': {
                'date': 1630987867, 'from_id': 134431423, 'id': 144, 'out': 0, 'peer_id': 134431423,
                'text': 'ПРИВЕТ', 'conversation_message_id': 141, 'fwd_messages': [], 'important': False,
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

    def test_run(self):
        count = 5
        obj = int
        events = [obj] * count
        longpoller_mock = Mock(return_value=events)
        longpoller_mock_listen_mock = Mock()
        longpoller_mock_listen_mock.listen = longpoller_mock
        logger_mock = Mock()
        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=longpoller_mock_listen_mock):
                bot = Bot('group_id', 'token', logger_mock)
                bot.on_event = Mock()
                bot.run()
                bot.on_event.assert_called()
                bot.on_event.assert_called_with(obj)
                result = bot.on_event.call_count
                self.assertEqual(result, count)

    def test_on_event(self):
        message = 'response'
        random.choice = Mock(return_value=message)
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_mock = Mock()
        logger_mock = Mock()
        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll'):
                bot = Bot('group_id', 'token', logger_mock)
                bot.api = Mock()
                bot.api.messages.send = send_mock
                bot.on_event(event)
            send_mock.assert_called_once_with(message=message,
                                              random_id=ANY,
                                              peer_id=self.RAW_EVENT['object']['message']['peer_id']
                                              )


if __name__ == '__main__':
    unittest.main()
