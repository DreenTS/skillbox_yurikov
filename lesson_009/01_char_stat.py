# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4
import zipfile


class Statter:

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat_dict = {}

    def unzip_file(self):
        zip_file = zipfile.ZipFile(self.file_name, 'r')
        for filename in zip_file.namelist():
            zip_file.extract(filename)
            self.file_name = filename

    def counter(self):
        if self.file_name.endswith('.zip'):
            self.unzip_file()
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                self._counter_for_one_line(line)
        self.stat_dict = dict(sorted(self.stat_dict.items(), key=lambda el: el[1], reverse=True))

    def _counter_for_one_line(self, line):
        for char in line:
            if char.isalpha():
                if char in self.stat_dict:
                    self.stat_dict[char] += 1
                else:
                    self.stat_dict[char] = 1


book_stat = Statter('python_snippets/voyna-i-mir.txt.zip')
book_stat.counter()

# TODO: сделайте вывод собранной информации методом Statter
print(f'+{"+":-^19}-+')
print(f'|{"длина":^9}|{"частота":^10}|')
print(f'+{"+":-^19}-+')
total = 0
for char, count in book_stat.stat_dict.items():
    print(f'|{char:^9}|{count:^10}|')
    total += count
print(f'+{"+":-^19}-+')
print(f'|{"итого":^9}|{total:^10}|')
print(f'+{"+":-^19}-+')
# TODO: и можно доделывать

# После зачета первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
