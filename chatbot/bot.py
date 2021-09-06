try:
    import settings
except ImportError:
    exit('DO cp settings.py.default settings.py and set token and group id!')

import random
from log_config import configure_logger
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

RESPONSES = [
    'Спасибо за ваше сообщение. Скоро вам ответят!',
    'Привет! Я бот и я уже передал человеку, что вы написали. Ждите ответа.',
    'У меня нет настроения, уйди.',
    'МОЯ НЕ ПОНИМАТЬ'
]


class Bot:
    """
    Чат-бот для vk.com

    Use python3.9
    """

    def __init__(self, group_id, token):
        """
        :param group_id: group id для группы vk.com
        :param token: token для группы vk.com
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        """
        Запуск бота.
        """
        for event in self.long_poller.listen():
            print('\nНОВОЕ СОБЫТИЕ:\n')
            try:
                self.on_event(event)
            except Exception:
                bot_logger.exception('При обработке события возникла ошибка.')

    def on_event(self, event):
        """
        Обработка событий из личных сообщений с сообществом.
        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            response = random.choice(RESPONSES)
            bot_logger.info(f'НОВОЕ СООБЩЕНИЕ : {event.object.message["text"]}')
            bot_logger.info(f'RESPONSE : {response}')
            self.api.messages.send(message=response,
                                   random_id=get_random_id(),
                                   peer_id=event.object.message['peer_id'])
        else:
            bot_logger.ERROR(f'Мы пока не умеем обрабатывать события типа {event.type}')


if __name__ == '__main__':
    bot_logger = configure_logger()
    group_id = settings.GROUP_ID
    token = settings.TOKEN
    bot = Bot(group_id=group_id, token=token)
    bot.run()

# зачет!
