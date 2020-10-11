# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
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
from multiprocessing import Process, Pipe


class CheckVolatility(Process):

    def __init__(self, dir_path, file_name, pipe, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dir_path = dir_path
        self.file_name = file_name
        self.maximum = 0
        self.minimum = 0
        self.half_sum = 0
        self.volatility = 0
        self.pipe = pipe

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
            self.pipe.send([self.file_name[:-4], self.volatility])
            self.pipe.close()


class Manager:

    def __init__(self, files, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files = files
        self.class_list = []
        self.zero_list = []
        self.processes = []
        self.pipes = []

    def manage(self):
        for dirpath, dirnames, filenames in os.walk(self.files):
            for filename in filenames:
                parent, child = Pipe()
                self.processes.append(CheckVolatility(dir_path=dirpath, file_name=filename, pipe=child))
                self.pipes.append(parent)
            for process in self.processes:
                process.start()
            for process in self.processes:
                process.join()
            for pipe in self.pipes:
                name, volatility = pipe.recv()
                if volatility != 0.0:
                    self.class_list.append([name, volatility])
                else:
                    self.zero_list.append(name)
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


if __name__ == '__main__':
    manager = Manager('trades')
    manager.manage()
