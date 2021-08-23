def data_check(data):
    default_set = set('-123456789/X')
    if len(data) != 20:
        raise ValueError('Количество фреймов должно быть равно 10')
    elif not set(data) <= default_set:
        raise ValueError('Неправильный набор символов')


def frames_check(frame_list):
    for f in frame_list:
        if f.isdigit() and sum(map(int, f)) >= 10:
            raise ValueError(f'Ошибка в записи фрейма "{f}"; сумма должна быть <= 9')
        elif '/' in f and f[0] in ['-', '/']:
            raise ValueError(f'Ошибка в записи фрейма "{f}"; "/" - spare, указывает на то, что выбиты оставшиеся кегли')


def get_score(game_result=None):
    if game_result is None:
        raise ValueError('Передано пустое значение дя подсчёта!')
    elif not isinstance(game_result, str):
        raise TypeError('Параметр game_result должен иметь тип "str"')

    # Замена русской буквы на латинскую (проверк на дурака)
    # Для удобства подсчёта очков: заменяем фрейм страйка 'X' на фрейм '-X'
    result = game_result.upper().replace('Х', 'X').replace('X', '-X')

    # Проверка данных на валидность
    data_check(data=result)
    frames = [result[i:i + 2] for i in range(0, len(result), 2)]
    frames_check(frame_list=frames)

    # Подсчёт очков
    total_scores = 0
    for frame in frames:
        if frame == '-X':
            total_scores += 20
        elif '/' in frame:
            total_scores += 15
        else:
            total_scores += sum(map(int, frame.replace('-', '0')))
    return total_scores


if __name__ == '__main__':
    try:
        game_result = '8/549-XX5/53629/9/'
        scores = get_score(game_result=game_result)
        print(f'Количество очков для результата "{game_result}" - {scores}.')
    except Exception as exc:
        print(f'{exc.__class__.__name__}: {exc}')
