# -*- coding: utf-8 -*-

# Создать модуль my_burger. В нем определить функции добавления инградиентов:
#  - булочки
#  - котлеты
#  - огурчика
#  - помидорчика
#  - майонеза
#  - сыра
# В каждой функции выводить на консоль что-то вроде "А теперь добавим ..."

# В этом модуле создать рецепт двойного чизбургера (https://goo.gl/zA3goZ)
# с помощью фукций из my_burger и вывести на консоль.

# Создать рецепт своего бургера, по вашему вкусу.
# Если не хватает инградиентов - создать соответствующие функции в модуле my_burger

import my_burger

print('Рецепт чизбургера.\n')
my_burger.bread(1)
my_burger.meat()
my_burger.cheese()
my_burger.meat()
my_burger.cheese()
my_burger.cucumber()
my_burger.tomato()
my_burger.mayonnaise()
my_burger.bread(2)
print('\nВот и всё, готово!\n')

print('Рецепт рашнбургера.\n')
my_burger.bread(1)
my_burger.mayonnaise()
my_burger.tomato()
my_burger.mayonnaise()
my_burger.tomato()
my_burger.mayonnaise()
my_burger.bread(2)
print('\nВот и всё, готово!')


