import state_handler


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


def get_score(game_result=None):
    if game_result is None:
        raise ValueError('Передано пустое значение дя подсчёта!')
    elif not isinstance(game_result, str):
        raise WrongTypeError

    # Замена русской буквы на латинскую (проверк на дурака)
    # Для удобства подсчёта очков: заменяем фрейм страйка 'X' на фрейм '-X'
    result = game_result.upper().replace('Х', 'X').replace('X', '-X')

    # Проверка данных на валидность
    data_check(data=result)
    frames = [result[i:i + 2] for i in range(0, len(result), 2)]
    frames_check(frame_list=frames)

    # Подсчёт очков
    # total_scores = 0
    # for frame in frames:
    #     if frame == '-X':
    #         total_scores += 20
    #     elif '/' in frame:
    #         total_scores += 15
    #     else:
    #         total_scores += sum(map(int, frame.replace('-', '0')))
    # return total_scores

    # Подсчёт очков для паттерна Состояние
    handler = state_handler.ScoreHandler(result=result)
    handler.count_score()
    return handler.total_score


if __name__ == '__main__':
    try:
        game_result = '8/549-XX5/53629/9/'
        scores = get_score(game_result=game_result)
        print(f'Количество очков для результата "{game_result}" - {scores}.')
    except Exception as exc:
        print(f'{exc.__class__.__name__}: {exc}')
