from collections import defaultdict, OrderedDict
import bowling


class FileHandler:

    def __init__(self, file_in_name, file_out_name):
        self.file_in = file_in_name
        self.file_out = file_out_name
        self.tours = defaultdict(dict)
        self.rejected = defaultdict(dict)

    def total_count(self):
        self._make_file_dict(self.file_in)
        for tour, players in self.tours.items():
            max_score, winner = 0, 'winner'
            for player, game_result in players.items():
                try:
                    self.tours[tour][player].append(bowling.get_score(game_result=game_result[0]))
                    if self.tours[tour][player][1] > max_score:
                        max_score = self.tours[tour][player][1]
                        winner = player
                except Exception as exc:
                    self.rejected[tour][player] = [game_result, exc]
                    self.tours[tour][player].append('ДИСКВАЛИФИЦИРОВАН')
            self.tours[tour]['winner'] = winner
        self._rejected_to_file()
        self._save_to_file(self.file_out)

    def _make_file_dict(self, file_name):
        curr_tour, splitted_line = 0, ''
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                if 'Tour' in line:
                    curr_tour += 1
                    self.tours[f'### Tour {curr_tour}'] = OrderedDict()
                elif 'winner' not in line:
                    splitted_line = line.split('\t')
                    self.tours[f'### Tour {curr_tour}'][splitted_line[0]] = [splitted_line[1][:-1], ]
                else:
                    file.readline()

    def _rejected_to_file(self):
        with open('rejected.txt', 'w', encoding='utf-8') as file:
            # TODO Хардкодить данные это плохая практика - создайте константу для имени файла
            file.write('Список дисквалифицированных.\n\n')
            for tour, players in self.rejected.items():
                file.write(f'{tour}\n')
                for player, result in players.items():
                    file.write(f'{player}\t{result[0][0]}\t{result[1]}\n')
                file.write('\n')

    def _save_to_file(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            for tour, players in self.tours.items():
                file.write(f'{tour}\n')
                for player, result in players.items():
                    if player != 'winner':
                        file.write(f'{player}\t{result[0]}\t{result[1]}\n')
                    else:
                        file.write(f'Winner is \t{result}\n')
                file.write('\n')


if __name__ == '__main__':
    try:
        handler = FileHandler(file_in_name='tournament.txt', file_out_name='tournament_result.txt')
        handler.total_count()
    except Exception as exc:
        print(f'{exc.__class__.__name__}: {exc}')
