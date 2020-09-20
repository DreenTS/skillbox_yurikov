# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4

class LogParser:

    def __init__(self, file_in_name, file_out_name):
        self.file_in = file_in_name
        self.file_out = file_out_name
        self.log_dict = {}

    def fill_dict(self, mode=1):

        """
            группировка вобытий
            mode=1  - по минутам
            mode=2  - по часам
            mode=3  - по месяцу
            mode=4  - по году
        """
        if mode not in range(1, 5):
            print('Ошибка при выборе типа группировки.')
        else:
            with open(self.file_in, 'r', encoding='cp1251') as file:
                for line in file:
                    self._fill_dict_for_line(line, mode=mode)

    def _fill_dict_for_line(self, line, mode=1):
        if mode == 1:
            n = 17
        elif mode == 2:
            n = 14
        elif mode == 3:
            n = 8
        else:
            n = 5
        if line[1:n] in self.log_dict:
            if line[-4] == 'N':
                self.log_dict[line[1:n]] += 1
        else:
            self.log_dict[line[1:n]] = 1

    def fill_file(self):
        with open(self.file_out, 'w', encoding='utf8') as file:
            for date, count in self.log_dict.items():
                file.write('[' + date + '] ' + str(count) + '\n')


parser = LogParser(file_in_name='events.txt', file_out_name='total_parse.txt')
# группировка по минутам
parser.fill_dict(mode=1)
parser.fill_file()
# группировка по часам
# parser.fill_dict(mode=2)
# parser.fill_file()
# # группировка по месяцу
# parser.fill_dict(mode=3)
# parser.fill_file()
# # группировка по году
# parser.fill_dict(mode=4)
# parser.fill_file()
print('Done!!! Check the file.')

# После зачета первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
