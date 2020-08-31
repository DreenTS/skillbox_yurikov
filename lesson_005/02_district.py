# -*- coding: utf-8 -*-

# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join

from district.central_street.house1 import room1 as central_h1_r1
from district.central_street.house1 import room2 as central_h1_r2
from district.central_street.house2 import room1 as central_h2_r1
from district.central_street.house2 import room2 as central_h2_r2
from district.soviet_street.house1 import room1 as soviet_h1_r1
from district.soviet_street.house1 import room2 as soviet_h1_r2
from district.soviet_street.house2 import room1 as soviet_h2_r1
from district.soviet_street.house2 import room2 as soviet_h2_r2

list_of_residents = []
for name in central_h1_r1.folks:
    list_of_residents.append(name)
for name in central_h1_r2.folks:
    list_of_residents.append(name)
for name in central_h2_r1.folks:
    list_of_residents.append(name)
for name in central_h2_r2.folks:
    list_of_residents.append(name)
for name in soviet_h1_r1.folks:
    list_of_residents.append(name)
for name in soviet_h1_r2.folks:
    list_of_residents.append(name)
for name in soviet_h2_r1.folks:
    list_of_residents.append(name)
for name in soviet_h2_r2.folks:
    list_of_residents.append(name)

# Никак не додумался, как ещё можно сделать. Если есть способ - подскажите плз.
print(', '.join(list_of_residents))
# зачет!