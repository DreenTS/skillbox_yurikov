# -*- coding: utf-8 -*-

# Создайте списки:

# моя семья (минимум 3 элемента, есть еще дедушки и бабушки, если что)
my_family = ['dad', 'mom', 'son', 'daughter']


# список списков приблизителного роста членов вашей семьи
my_family_height = [
    [my_family[0], 182],
    [my_family[1], 160],
    [my_family[2], 171],
    [my_family[3], 166],
]

# Выведите на консоль рост отца в формате
#   Рост отца - ХХ см

print('Рост отца -', my_family_height[0][1], 'см')

# Выведите на консоль общий рост вашей семьи как сумму ростов всех членов
#   Общий рост моей семьи - ХХ см
summ = 0
for i in my_family_height:
    summ += i[1]
print('Общий рост моей семьи -', summ, 'см')

# зачет!