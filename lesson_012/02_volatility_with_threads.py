# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#

import os
import time
from threading import Thread


class CheckVolatility(Thread):

    def __init__(self, dir_path, file_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir_path = dir_path
        self.file_name = file_name
        self.maximum = 0
        self.minimum = 0
        self.half_sum = 0
        self.volatility = 0

    def run(self):
        with open(os.path.join(self.dir_path, self.file_name), 'r', encoding='utf8') as file:
            file.readline()
            temp_list = []
            for line in file:
                temp_list.append(float(line.split(',')[2]))
            self.maximum = max(temp_list)
            self.minimum = min(temp_list)
            self.half_sum = (self.maximum + self.minimum) / 2
            self.volatility = ((self.maximum - self.minimum) / self.half_sum) * 100


class Manager(Thread):  # TODO: это не обязательно запускать в отдельном треде

    def __init__(self, files, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files = files
        self.class_list = []
        self.zero_list = []
        self.threads = []

    def run(self):
        for dirpath, dirnames, filenames in os.walk(self.files):
            for filename in filenames:
                self.threads.append(CheckVolatility(dir_path=dirpath, file_name=filename))
            for thread in self.threads:
                thread.start()
            for thread in self.threads:
                thread.join()
            for thread in self.threads:
                if thread.volatility != 0.0:
                    self.class_list.append([thread.file_name[:-4], thread.volatility])
                else:
                    self.zero_list.append(thread.file_name[:-4])
        self.show_volatility()

    def show_volatility(self):
        self.class_list.sort(key=lambda i: i[1])
        self.class_list.reverse()
        print('Максимальная волатильность:')
        for ticker in self.class_list[:3]:
            print(f'{ticker[0]} - {round(ticker[1], 3)} %')
        print('\nМинимальная волатильность:')
        for ticker in self.class_list[-3:]:
            print(f'{ticker[0]} - {round(ticker[1], 3)} %')
        print('\nНулевая волатильность:')
        self.zero_list.sort()
        print(','.join(self.zero_list))


tt = time.time()
manager = Manager('trades')
manager.start()
manager.join()
print(time.time() - tt)
