def get_score(game_result='--------------------'):
    if not isinstance(game_result, str):
        raise TypeError('параметр game_result должен иметь тип "str"')

    # Замена русской буквы на латинскую (проверк на дурака)
    # Для удобства подсчёта очков: заменяем фрейм страйка 'X' на фрейм '-X'
    result = game_result.upper().replace('Х', 'X').replace('X', '-X')

