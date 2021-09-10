
class Player:

    def __init__(self, name, data_dict):
        self.name = name
        self.loc, self.exp, self.date = data_dict.values()


class DungeonMaster:

    def __init__(self, player, map):
        self.player = player
        self.map = map

    def tell(self):
        pass

    def _game(self):
        pass

    def _start(self):
        pass

    def _lose(self):
        pass

    def _end(self):
        pass


if __name__ == '__main__':
    master = DungeonMaster(player='Nick', map='map')
    master.tell()