from abc import ABC, abstractmethod


class State(ABC):

    @abstractmethod
    def private_count(self, char):
        pass

    @abstractmethod
    def public_count(self, char):
        pass


class FirstThrow(State):

    def __init__(self):
        self.res = 0

    def private_count(self, char):
        if char != '-':
            self.res = int(char)
        return SecondThrow(), self.res

    def public_count(self, char):
        pass


class SecondThrow(State):

    def __init__(self):
        self.res = 0

    def private_count(self, char):
        if char == 'X':
            self.res = 20
        elif char == '/':
            self.res = 15
        elif char != '-':
            self.res = int(char)
        return FirstThrow(), self.res

    def public_count(self, char):
        pass


class ScoreHandler:

    def __init__(self, result, mode):
        self.result = result
        self.mode = mode
        self.state = None
        self.total_score = 0

    def count_score(self):
        self.state, prev, curr = FirstThrow(), 0, 0
        if self.mode == 'private':
            for char in self.result:
                self.state, curr = self.state.private_count(char=char)
                if curr in [15, 20]:
                    self.total_score += curr - prev
                else:
                    self.total_score += curr
                prev = curr
        else:
            pass
