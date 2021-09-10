import datetime
import os
import time
from decimal import Decimal, getcontext
import re


class Player:

    def __init__(self, name, data_dict):
        self.name = name
        self.loc, self.exp, self.date = data_dict.values()


class DungeonMaster:

    def __init__(self, player, dung_map, time):
        self.player = player
        self.map = dung_map[self.player.loc]
        self.str_remaining_time = time
        self._str_to_decimal_time()
        self._time_pattern = r'tm\d*\.{,1}\d*'
        self._exp_pattern = r'exp\d*\.{,1}\d*'

    def tell(self):
        self._start()
        while self.player.loc != 'Hatch_tm159.098765432':
            if self.decimal_remaining_time <= Decimal(0.0):
                self._lose()
                return
            else:
                self._game()

    def _str_to_decimal_time(self):
        getcontext().prec = 10
        self.decimal_remaining_time = Decimal('123456.0987654321')

    def _game(self):
        print(f'Вы находитесь в локации {self.player.loc}. Что дальше?')
        for i, point in enumerate(self.map):
            if isinstance(point, dict):
                print(f'{i + 1}. Перейти в локацию {list(point.keys())[0]}. '
                      f'На это уйдёт {self._get_time_from_pattern(re_str=point)} секунд.')
            else:
                print(f'{i + 1}. Атаковать {point} за {self._get_exp_from_pattern(re_str=point)} опыта. '
                      f'Требуется времени для битвы: {self._get_time_from_pattern(re_str=point)}.')

        choice = int(input('Выберите действие (номер): ')) - 1
        if isinstance(choice, int) and choice in range(len(self.map) + 1):
            action = self.map[choice]
            temp_time = self._get_time_from_pattern(re_str=action)
            self.player.date = str(datetime.timedelta(float(temp_time)))
            self.decimal_remaining_time -= Decimal(temp_time)
            if isinstance(action, dict):
                self._travel(action=action)
            else:
                self._fight(action=action)
            os.system('cls')
        else:
            print('\nПохоже, вы написали неправильный номер. Давайте попробуем ещё раз...')
            for _ in range(3):
                print('.', end='')
                time.sleep(1.5)
            os.system('cls')

    def _get_time_from_pattern(self, re_str):
        if isinstance(re_str, dict):
            return re.search(self._time_pattern, list(re_str.keys())[0]).group()[2:]
        else:
            return re.search(self._time_pattern, re_str).group()[2:]

    def _get_exp_from_pattern(self, re_str):
        return re.search(self._exp_pattern, re_str).group()[3:]

    def _travel(self, action):
        self.player.loc = list(action.keys())[0]
        self.map = action[self.player.loc]

    def _fight(self, action):
        self.player.exp += int(self._get_exp_from_pattern(re_str=action))
        self.map.remove(action)

    def _start(self):
        print('start')

    def _lose(self):
        self._str_to_decimal_time()
        print('lose')

    def _is_win(self):
        if self.player.loc == 'Hatch_tm159.098765432':
            if self.player.exp == 280:
                return True
        else:
            return False


if __name__ == '__main__':
    dungeon_map = {'Location_0_tm0': []}
    master = DungeonMaster(player='Nick', dung_map=dungeon_map, time='123456.0987654321')
    master.tell()
