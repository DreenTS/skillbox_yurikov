# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>  # Итератор или генератор? выбирайте что вам более понятно
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234


# Решение генератором

def log_parser(file_name):
    log_dict = {}
    temp_line = ''
    with open(file_name, 'r', encoding='cp1251') as file:
        for line in file:
            if temp_line != line[1:17] and temp_line:
                yield temp_line, log_dict[temp_line]
            temp_line = line[1:17]
            if temp_line not in log_dict:
                log_dict[temp_line] = 0
            if line[-4] == 'N':
                log_dict[temp_line] += 1


grouped_events = log_parser(file_name='events.txt')
for group_time, event_count in grouped_events:
    print(f'[{group_time}] {event_count}')


# Решение итератором

# class LogParser:
#
#     def __init__(self, file_name):
#         self.file_in = file_name
#         self.log_dict = {}
#         self.file = None
#         self.line = ''
#
#     def __iter__(self):
#         self.file = open(self.file_in, 'r', encoding='cp1251')
#         self.line = self.file.readline()
#         return self
#
#     def __next__(self):
#         temp_line = self.line[1:17]
#         while temp_line == self.line[1:17]:
#             if not self.line:
#                 self.file.close()
#                 raise StopIteration
#             if self.line[1:17] not in self.log_dict:
#                 self.log_dict[self.line[1:17]] = 0
#             if self.line[-4] == 'N':
#                 self.log_dict[temp_line] += 1
#             self.line = self.file.readline()
#         return temp_line, self.log_dict[temp_line]
#
#
# grouped_events = LogParser(file_name='events.txt')
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
# зачет!