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
            for player, game_result in players.items():
                try:
                    self.tours[tour][player].append(bowling.get_score(game_result=game_result[0]))
                except Exception as exc:
                    self.rejected[tour][player] = [game_result, exc]
                    self.tours[tour][player].append('ДИСКВАЛИФИЦИРОВАН')

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


handler = FileHandler(file_in_name='tournament.txt', file_out_name='tournament_result.txt')
handler.total_count()