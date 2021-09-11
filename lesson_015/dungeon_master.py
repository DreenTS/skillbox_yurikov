import csv
import datetime
import os
import sys
import time
from project_settings import *
from copy import deepcopy
from decimal import Decimal, getcontext
import re

from termcolor import cprint
import colorama

colorama.init()


class DungeonMaster:
    """
    DungeonMaster - мастер подземелья.

    Инициализирует данные для игровой сессии(-ий), а именно:

    - имена полей для вывода в .csv
    - игрока (текущие имя, локацию, опыт, дату)
    - карту подземелья
    - время на игру
    - паттерны регулярных выражений для поиска tm времени и exp опыта в событиях карты.

    Запускает игровую сессию и управляет ей. Подробнее см. docstrings методов класса.
    """

    def __init__(self, data_dict, dung_map):
        self.field_names = FIELD_NAMES_FOR_CSV_FILE
        self.origin_data = [data_dict, dung_map, REMAINING_TIME]
        self.player = {'name': self.origin_data[0]['name'],
                       'current_location': self.origin_data[0]['current_location'],
                       'current_experience': self.origin_data[0]['current_experience'],
                       'current_date': self.origin_data[0]['current_date'],
                       }
        self.map = deepcopy(self.origin_data[1][self.player['current_location']])
        self.str_remaining_time = self.origin_data[2]
        self._str_to_decimal_time()
        self._time_pattern = TIME_PATTERN_FOR_JSON
        self._exp_pattern = EXP_PATTERN_FOR_JSON
        self.save_to = CSV_FILENAME_TO_SAVE

    def tell(self):
        """
        Запуск игровой сессии ("рассказывай" в духе мастера подземелий, не так ли?).
        Вызывает метод для вывода приветственного текста. Инициализирует цикл (метод self._win() см. ниже).
        Вызывает метод проигрыша, если время на прохождение истекло, иначе метод процесса игры.
        При выходе из цикда (победе) вызывает метод сохранения результата игры в файл, см. self._save_result()

        :return: None
        """
        self._start()
        self._dots()
        while not self._is_win():
            if self.decimal_remaining_time <= Decimal(0.0):
                self._lose()
            else:
                self._game()
        else:
            print('Ну наконец-то! Ты выбрался наружу... Ну ладно, беги давай. Твоя награда - твоя жизнь.')
            self._save_result()

    def _str_to_decimal_time(self):
        """
        Присваивает значение переменной времени на игру Decimal, для повышенной точности.

        :return: None
        """
        getcontext().prec = 50
        self.decimal_remaining_time = Decimal('123456.0987654321')

    def _game(self):
        """
        Процесс самой игры.
        Вывод текущей статистики игрока.
        Вызов метода self._lose() при заходе в тупик (когда на карте нет ни перехода в следующую локацию,
        ни монстра для битвы).
        Вывод доступных путей (выборов) для игрока: показывает текущих монстров или переходы в локации,
        давая игроку выбрать путь вводом числа.
        Все выборы пронумерованы.
        При выборе перехода в другую локацию вызывает метод self._travel(), при выборе битвы с монстром - self._fight()
        Увеличивает значение переменной времени игры и уменьшает значение переменной оставшегося на игру времени
        после выбора игрока.
        При вводе числа не из списка представленных выборов, любого другого неподходящего символа или при нажатии Enter
        позволяет повторить попытку ввода бесчисленное количество раз.
        Очищает экран перед возвратом в цикл метода self.tell()

        :return: None
        """
        self._print_stats()
        if len(self.map) == 0:
            print(f'\nХа-ха! Ты в тупике и монстров не осталось. Кажется, твоя песенка спета', end='')
            self._dots()
            self._lose()
            return
        print(f'\nТы находишься в локации {self.player["current_location"]}. Что дальше?')
        for i, point in enumerate(self.map):
            if isinstance(point, dict):
                print(f'{i + 1}. Перейти в локацию {list(point.keys())[0]}. '
                      f'На это уйдёт {self._get_time_from_pattern(re_str=point)} секунд.')
            else:
                print(f'{i + 1}. Атаковать {point} за {self._get_exp_from_pattern(re_str=point)} опыта. '
                      f'Требуется времени для битвы: {self._get_time_from_pattern(re_str=point)}.')
        try:
            choice = int(input('Выберите действие (номер): ')) - 1
        except ValueError:
            print('Похоже, ты написал неправильный номер. Давай попробуем ещё раз', end='')
            self._dots()
        else:
            if isinstance(choice, int) and choice in range(len(self.map) + 1):
                action = self.map[choice]
                temp_time = self._get_time_from_pattern(re_str=action)
                self.player['current_date'] += datetime.timedelta(seconds=float(temp_time))
                self.decimal_remaining_time -= Decimal(temp_time)
                if isinstance(action, dict):
                    self._travel(action=action)
                else:
                    self._fight(action=action)
                os.system('cls')
            else:
                print('Похоже, Ты написал неправильный номер. Давай попробуем ещё раз', end='')
                self._dots()

    def _print_stats(self):
        """
        Вывод текущей статистики игрока: имя, опыт, прошедшего и оставшегося времени.
        Добавлен цветной вывод, просто для красоты.

        :return: None
        """
        cprint(f'{self.player["name"]}', color='green')
        cprint(f'EXP = {self.player["current_experience"]} / 280', color='cyan')
        cprint(f'Прошло времени: {self.player["current_date"]}', color='yellow')
        cprint(f'Осталось секунд на прохождение: {self.decimal_remaining_time}', color='blue')

    def _get_time_from_pattern(self, re_str):
        """
        Возвращает строковое значение времени из значения события (локация или монстр)
        по паттерну, используя re.search()
        Если была выбрана локация, она имеет тип dict, если монстр - str
        Сохранение типа dict необходимо для переопределения карты переменной self.map

        :param re_str: str, dict, значение события (выбор игрока) с карты - Location..., Mob..., Boss...
        :return: str, строковое значение времени из значения события по паттерну
        """
        if isinstance(re_str, dict):
            return re.search(self._time_pattern, list(re_str.keys())[0]).group()[2:]
        else:
            return re.search(self._time_pattern, re_str).group()[2:]

    def _get_exp_from_pattern(self, re_str):
        """
        Возвращает строковое значение опыта из значения события (монстр)
        по паттерну, используя re.search()

        :param re_str: str, значение события битвы с монстром - Mob..., Boss...
        :return: str, строковое значение опыта из значения события по паттерну
        """
        return re.search(self._exp_pattern, re_str).group()[3:]

    def _travel(self, action):
        """
        Метод "путешествия".
        Меняет текущую локацию игрока на выбранную, переопределяет карту self.map,
        присваивая значения пришедшего словаря.

        :param action: dict, словарь локации, в которую будет сделано перемещение
        :return: None
        """
        self.player['current_location'] = list(action.keys())[0]
        self.map = action[self.player['current_location']]

    def _fight(self, action):
        """
        Метод "битвы".
        Увеличивает значение переменной опыта игрока на величину, полученную по поттерну при помощи re.search()
        из строки события (монстра).
        Удаляет с карты монстра на данную сессию.

        :param action: str, значение события битвы с монстром - Mob..., Boss...
        :return: None
        """
        self.player['current_experience'] += int(self._get_exp_from_pattern(re_str=action))
        self.map.remove(action)

    def _start(self):
        """
        Выводит приветственный текст с правилами игры.
        Ожидает ввода для запуска игры.

        :return: None
        """
        print('Очнулся, наконец?\n'
              'Меня зовут Мастер Подземелья (не спрашивай, почему и как я получил такое имя).'
              'Ты находишься в глубинах моего, собственно, Подземелья.\n'
              'Давай сыграем с тобой в игру? Ай, что я тебя спрашиваю... Хочешь жить - будешь играть.\n'
              'Правила просты: я постепенно буду затапливать коридоры Подземелья водой.\n'
              'Ты ведь не отрастил себе жабры, да? Отлично.\n'
              'В Подземелье куча ходов и злобных монстров...но выход один.\n'
              'Н а й д и   е г о .\n'
              'И я не советую тебе пропускать всех монстров - люк не откроется, '
              'если у тебя не будет 280 очков опыта (EXP). Опыт добудешь как раз с монстрятины.\n'
              'Ах да, насчёт воды - у тебя 123456.0987654321 секунд на то, чтобы сбежать отсюда.\n'
              'Думай основательно, в твоём случае время - золото. Точнее, жизнь.\n'
              'И да, пока не найдёшь люк (с нужным количеством опыта), я буду тебя воскрешать снова и снова...\n'
              'Ну что же, поехали!\n'
              'Нажми Enter.')
        _ = input()

    def _lose(self):
        """
        Метод проигрыша.
        Даёт игроку выбор: попробовать пройти подземелье сначала ещё раз или завершить игру.
        При выборе первого варианта заново инициализирует данные для игры и перезапускает её вызовом метода self.tell()
        При выборе второго варианта начинает запись результатов игры в файл, см. self._save_result()
        При любом выборе очищает экран.

        :return: None
        """
        print('Подземелье затопило и ты не смог выбраться. Попробуем ещё раз?')
        print('1. Да\n2. Нет')
        try:
            choice = int(input('Выберите действие (номер): '))
        except ValueError:
            print('Похоже, ты написал неправильный номер. Давай попробуем ещё раз', end='')
            self._dots()
        else:
            if choice == 1:
                print('Ну, ещё одна попытка, удачи', end='')
                self._dots()
                self._str_to_decimal_time()
                self.player['current_location'] = self.origin_data[0]['current_location']
                self.player['current_experience'] = self.origin_data[0]['current_experience']
                self.player['current_date'] = self.origin_data[0]['current_date']
                self.map = deepcopy(self.origin_data[1][self.player['current_location']])
                self.str_remaining_time = self.origin_data[2]
                self.tell()
                os.system('cls')
            elif choice == 2:
                print('Ты решил сдаться... Ну что же, твоё право. Твоя смерть будет увековечена в файле dungeon.csv .\n'
                      'Прощай!')
                self._dots()
                self._save_result()
            else:
                print('Похоже, Ты написал неправильный номер. Давай попробуем ещё раз', end='')
                self._dots()

    def _is_win(self):
        """
        Проверяет, выиграл ли игрок (нашёл люк, имеет нужное колличество опыта).
        Если люк найден, но опыта не хватает - вызывает метод self._lose()

        :return: bool
        """
        if self.player['current_location'] == 'Hatch_tm159.098765432':
            if self.player['current_experience'] == 280:
                return True
            else:
                print(f'Для открытия люка тебе необходим иметь 280 EXP. Твоё количество EXP: '
                      f'{self.player["current_experience"]}. '
                      f'Попробуем ещё раз', end='')
                self._dots()
                self._lose()
        else:
            return False

    def _dots(self):
        """
        Вспомогательный метод.
        Выводит на экран точки с задержкой и очищает экран.

        :return: None
        """
        for _ in range(3):
            print('.', end='')
            time.sleep(1.5)
        os.system('cls')

    def _save_result(self):
        """
        Метод сохранения результатов игры в файл .csv
        Завершает игру.

        :return: None
        """
        with open(self.save_to, 'w', newline='', encoding='utf-8') as out_csv:
            writer = csv.DictWriter(out_csv, delimiter=',', fieldnames=self.field_names)
            writer.writeheader()
            writer.writerow(self.player)
        sys.exit()


if __name__ == '__main__':
    dungeon_map = {'Location_0_tm0': []}
    master = DungeonMaster(data_dict={}, dung_map=dungeon_map)
    master.tell()
