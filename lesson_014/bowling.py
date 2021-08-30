import state_handler

RULES = {
    'private': 'внутреннего',
    'public': 'внешнего'
}


class FrameLengthError(Exception):

    def __str__(self):
        return 'Количество фреймов должно быть равно 10'


class WrongCharSetError(Exception):

    def __str__(self):
        return 'Неправильный набор символов'


class WrongTypeError(Exception):

    def __str__(self):
        return 'Параметр game_result должен иметь тип "str"'


class FrameSumError(Exception):

    def __init__(self, f):
        self.f = f

    def __str__(self):
        return f'Ошибка в записи фрейма "{self.f}"; сумма должна быть <= 9'


class SpareError(Exception):

    def __init__(self, f):
        self.f = f

    def __str__(self):
        return f'Ошибка в записи фрейма "{self.f}"; "/" - spare, указывает на то, что выбиты оставшиеся кегли'


class WrongModeError(Exception):

    def __str__(self):
        return 'Задан неверный режим. Возможные режимы: "private" (внутренний рынок), "public" (внешний рынок).'


def data_check(data):
    default_set = set('-123456789/X')
    if len(data) != 20:
        raise FrameLengthError
    elif not set(data) <= default_set:
        raise WrongCharSetError


def frames_check(frame_list):
    for f in frame_list:
        if f.isdigit() and sum(map(int, f)) > 10:
            raise FrameSumError(f=f)
        elif '/' in f and f[0] in ['-', '/']:
            raise SpareError(f=f)


def get_score(game_result=None, mode='private'):
    if game_result is None:
        raise ValueError('Передано пустое значение дя подсчёта!')
    elif not isinstance(game_result, str):
        raise WrongTypeError
    elif mode.lower() not in RULES.keys():
        raise WrongModeError

    # Замена русской буквы на латинскую (проверк на дурака)
    # Для удобства подсчёта очков: заменяем фрейм страйка 'X' на фрейм '-X'
    result = game_result.upper().replace('Х', 'X').replace('X', '-X')

    # Проверка данных на валидность
    data_check(data=result)
    frames = [result[i:i + 2] for i in range(0, len(result), 2)]
    frames_check(frame_list=frames)

    # Оставил подсчёт только на Состояниях, с классами проще работать

    # Подсчёт очков для паттерна Состояние
    handler = state_handler.ScoreHandler(result=result, mode=mode.lower())
    handler.count_score()
    return handler.total_score


if __name__ == '__main__':
    try:
        game_result = '8/549-XX5/53629/9/'
        mode = 'public'
        scores = get_score(game_result=game_result, mode=mode)
        print(f'Количество очков для результата "{game_result}" - {scores}.'
              f'Подсчёт очков был произведён согласно правилам {RULES[mode]} рынка.')
    except Exception as exc:
        print(f'{exc.__class__.__name__}: {exc}')
