import csv
import datetime
import os
import sys
import time
from copy import deepcopy
from decimal import Decimal, getcontext
import re

from termcolor import cprint
import colorama
colorama.init()


class DungeonMaster:

    def __init__(self, data_dict, dung_map, time):
        self.field_names = ['name', 'current_location', 'current_experience', 'current_date']
        self.origin_data = [data_dict, dung_map, time]
        self.player = {'name': self.origin_data[0]['name'],
                       'current_location': self.origin_data[0]['current_location'],
                       'current_experience': self.origin_data[0]['current_experience'],
                       'current_date': self.origin_data[0]['current_date'],
                       }
        self.map = deepcopy(self.origin_data[1][self.player['current_location']])
        self.str_remaining_time = self.origin_data[2]
        self._str_to_decimal_time()
        self._time_pattern = r'tm\d*\.{,1}\d*'
        self._exp_pattern = r'exp\d*\.{,1}\d*'
        self.save_to = 'dungeon.csv'

    def tell(self):
        self._start()
        self._dots()
        while not self._is_win():
            if self.decimal_remaining_time <= Decimal(0.0):
                self._lose()
            else:
                self._game()

    def _str_to_decimal_time(self):
        getcontext().prec = 50
        self.decimal_remaining_time = Decimal('123456.0987654321')

    def _game(self):
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
        cprint(f'{self.player["name"]}', color='green')
        cprint(f'EXP = {self.player["current_experience"]} / 280', color='cyan')
        cprint(f'Прошло времени: {self.player["current_date"]}', color='yellow')
        cprint(f'Осталось секунд на прохождение: {self.decimal_remaining_time}', color='blue')

    def _get_time_from_pattern(self, re_str):
        if isinstance(re_str, dict):
            return re.search(self._time_pattern, list(re_str.keys())[0]).group()[2:]
        else:
            return re.search(self._time_pattern, re_str).group()[2:]

    def _get_exp_from_pattern(self, re_str):
        return re.search(self._exp_pattern, re_str).group()[3:]

    def _travel(self, action):
        self.player['current_location'] = list(action.keys())[0]
        self.map = action[self.player['current_location']]

    def _fight(self, action):
        self.player['current_experience'] += int(self._get_exp_from_pattern(re_str=action))
        self.map.remove(action)

    def _start(self):
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
        if self.player['current_location'] == 'Hatch_tm159.098765432':
            if self.player['current_experience'] == 280:
                print('Ну наконец-то! Ты выбрался наружу... Ну ладно, беги давай. Твоя награда - твоя жизнь.')
                self._save_result()
            else:
                print(f'Для открытия люка тебе необходим иметь 280 EXP. Твоё количество EXP: '
                      f'{self.player["current_experience"]}. '
                      f'Попробуем ещё раз', end='')
                self._dots()
                self._lose()
        else:
            return False

    def _dots(self):
        for _ in range(3):
            print('.', end='')
            time.sleep(1.5)
        os.system('cls')

    def _save_result(self):
        with open(self.save_to, 'w', newline='', encoding='utf-8') as out_csv:
            writer = csv.DictWriter(out_csv, delimiter=',', fieldnames=self.field_names)
            writer.writeheader()
            writer.writerow(self.player)
        sys.exit()


if __name__ == '__main__':
    dungeon_map = {'Location_0_tm0': []}
    master = DungeonMaster(data_dict={}, dung_map=dungeon_map, time='123456.0987654321')
    master.tell()
