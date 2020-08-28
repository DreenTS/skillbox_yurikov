# -*- coding: utf-8 -*-

# Вывести на консоль жителей комнат (модули room_1 и room_2)
# Формат: В комнате room_1 живут: ...

import room_1, room_2

print('В комнате room_1 живут:')
for name in enumerate(room_1.folks):
    print(name[0] + 1, name[1])
print('\nВ комнате room_2 живут:')
for name in enumerate(room_2.folks):
    print(name[0] + 1, name[1])
