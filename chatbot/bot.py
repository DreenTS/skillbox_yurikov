import datetime

import handlers

try:
    import settings
except ImportError:
    exit('DO cp settings.py.default settings.py and set token and group id!')

import random
from log_config import configure_logger
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class UserState:
    """
    Состояние пользователя внутри сценария.
    """
    def __init__(self, scenario_name, step_name, context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}


class Bot:
    """
    Чат-бот для vk.com

    Use python3.9
    """

    def __init__(self, group_id, token, logger):
        """
        :param group_id: group id для группы vk.com
        :param token: token для группы vk.com
        """
        self.group_id = group_id
        self.token = token
        self.bot_logger = logger
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.user_states = dict()  # user_id -> UserState

    def run(self):
        """
        Запуск бота.
        """
        for event in self.long_poller.listen():
            print('\nНОВОЕ СОБЫТИЕ:\n')
            try:
                self.on_event(event)
            except Exception:
                self.bot_logger.exception('При обработке события возникла ошибка.')

    def on_event(self, event):
        """
        Обработка событий из личных сообщений с сообществом.
        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type != VkBotEventType.MESSAGE_NEW:
            self.bot_logger.ERROR(f'Мы пока не умеем обрабатывать события типа {event.type}')
        user_id = event.object.message['peer_id']
        user_text = event.object.message["text"].lower()
        for intent in settings.INTENTS:
            if user_text == intent['command']:
                if user_id in self.user_states:
                    self.user_states.pop(user_id)
                if intent['answer']:
                    response = intent['answer']
                else:
                    response = self.start_scenario(user_id=user_id, scenario=intent['scenario'])
                break
        else:
            if user_id in self.user_states:
                response = self.continue_scenario(user_id=user_id, user_text=user_text)
            else:
                response = random.choice(settings.DEFAULT_ANSWERS)

        self.bot_logger.info(f'НОВОЕ СООБЩЕНИЕ : {user_text}')
        self.bot_logger.info(f'RESPONSE : {response}')
        self.api.messages.send(message=response,
                               random_id=random.randint(0, 2 ** 10000),
                               peer_id=user_id)

    def start_scenario(self, user_id, scenario):
        step = settings.SCENARIOS[scenario]['first_step']
        self.user_states[user_id] = UserState(scenario_name=scenario, step_name=step)
        result = settings.SCENARIOS[scenario]['steps'][step]['text']
        return result

    def continue_scenario(self, user_id, user_text):
        state = self.user_states[user_id]

        steps = settings.SCENARIOS[state.scenario_name]['steps']
        curr_step = steps[state.step_name]

        handler = getattr(handlers, curr_step['handler'])
        if handler.__name__ == 'city_handler':
            args = (user_text, state.context, state.step_name[0])
        else:
            args = (user_text, state.context)
        if handler(*args):
            next_step = steps[curr_step['next_step']]
            if next_step['next_step']:
                state.step_name = curr_step['next_step']
            else:
                result = next_step['text']
                self.user_states.pop(user_id)
                return result
            result = self.extra_print(state=state, step=state.step_name)
            if 'Подход' in result:
                self.user_states.pop(user_id)
            else:
                result += steps[state.step_name]['text']
        else:
            if handler.__name__ == 'data_checking_handler':
                self.user_states.pop(user_id)
            result = curr_step['failure_text']
        return result

    def extra_print(self, state, step):
        context = state.context
        res = ''
        if '4' in step:
            context['tickets'] = []
            from_city = context['departure_city']
            to_city = context['arrival_city']
            disp_res = self.dispatcher(context=context, from_city=from_city, to_city=to_city)
            if disp_res == '':
                res += 'Подходящих рейсов нет. Попробуйте поиск с другими данными. Введите /ticket'
            else:
                res += disp_res
        elif '7' in step:
            res += f'Проверка данных авиабилета (стоимость билета указана за одно место):\n....' \
                   f'Откуда: {context["departure_city"].capitalize()}\n....' \
                   f'Куда: {context["arrival_city"].capitalize()}\n....' \
                   f'Дата: {context["flight"]["date"]}\n....Стоимость билета: {context["flight"]["price"]}\n....' \
                   f'Количество мест: {context["number_of_seats"]}\n....' \
                   f'Комментарий: {context["comment"]}\n\n'
        return res

    def dispatcher(self, context, from_city, to_city):
        flights_list = [list(key.values()) for key in settings.FLIGHTS[from_city][to_city]]
        today = datetime.datetime.today().date()
        user_date_datetime_format = datetime.datetime.strptime(context['date'], '%d-%m-%Y').date()
        res = ''
        for i, flight in enumerate(flights_list):
            only_date = datetime.datetime.strptime(flight[0][:-6], '%d-%m-%Y').date()
            if only_date - today >= datetime.timedelta(days=10):
                if abs(only_date - user_date_datetime_format) <= datetime.timedelta(days=10):
                    temp_ticket = f'Дата: {flight[0]}\n....Стоимость билета: {flight[1]}'
                    res += f'{i + 1})\n....{temp_ticket}\n\n'
        return res


if __name__ == '__main__':
    bot_logger = configure_logger()
    group_id = settings.GROUP_ID
    token = settings.TOKEN
    bot = Bot(group_id=group_id, token=token, logger=bot_logger)
    bot.run()

# зачет!
