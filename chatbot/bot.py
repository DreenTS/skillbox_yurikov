import random
from my_token import TOKEN
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
            except Exception as exc:
                print(exc)

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(f'{event.type} : {event.object.message["text"]}')
            self.api.messages.send(message=random.choice(RESPONSES),
                                   random_id=get_random_id(),
                                   peer_id=event.object.message['peer_id'])
        else:
            print(f'Мы пока не умеем обрабатывать события типа {event.type}')


if __name__ == '__main__':
    group_id = 200346432
    bot = Bot(group_id=group_id, token=TOKEN)
    bot.run()

# зачет!
