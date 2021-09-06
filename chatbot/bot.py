import random
from my_token import TOKEN
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

    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            print('\nНОВОЕ СОБЫТИЕ:\n')
            try:
                self.on_event(event)
            except Exception:
                bot_logger.exception('При обработке события возникла ошибка.')

    def on_event(self, event):
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
    group_id = 200346432
    bot = Bot(group_id=group_id, token=TOKEN)
    bot.run()

# зачет!
