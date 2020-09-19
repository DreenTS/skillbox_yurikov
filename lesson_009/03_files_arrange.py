# -*- coding: utf-8 -*-

import os
import time
import shutil


# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени последней модификации файла
# (время создания файла берется по разному в разых ОС - см https://clck.ru/PBCAX - поэтому берем время модификации).
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником ОС в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит, см .gitignore в папке ДЗ)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4


class IconsSorter:

    def __init__(self, dir_in_name, dir_out_name):
        self.dir_in = os.path.normpath(dir_in_name)
        self.dir_out = os.path.normpath(dir_out_name)

    def scan_and_sort(self, name=None):
        if name is None:
            name = self.dir_in
        for dirpath, dirnames, filenames in os.walk(name):
            if dirnames:
                for dir in dirnames:
                    self.scan_and_sort(os.path.join(name, dir))
            if filenames:
                self._scan_and_sort_for_file(dirpath, filenames)

    def _scan_and_sort_for_file(self, dirpath, filenames):
        for file in filenames:
            file_time = os.path.getmtime(os.path.join(dirpath, file))
            right_file_time = time.gmtime(file_time)
            temp_path = os.path.join(self.dir_out, str(right_file_time[0]), str(right_file_time[1]))
            if not os.path.isdir(temp_path):
                os.makedirs(temp_path)
                shutil.copy2(os.path.join(dirpath, file), temp_path)
            else:
                shutil.copy2(os.path.join(dirpath, file), temp_path)


sorter = IconsSorter(dir_in_name='icons', dir_out_name='icons_by_year')
sorter.scan_and_sort()
print('Done!!!')

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится только к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html
# зачет!