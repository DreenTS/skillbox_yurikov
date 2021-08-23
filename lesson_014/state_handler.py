from abc import ABC, abstractmethod


class State(ABC):

    @abstractmethod
    def count(self, frame):
        pass


class FirstState(State):

    def __init__(self):
        self.score = 0

    def count(self, frame):
        self.score = 0
        if frame[0] != '-':
            self.score = int(frame[0])


class SecondState(State):

    def __init__(self):
        self.score = 0

    def count(self, frame):
        self.score = 0
        if frame[1] == '/':
            self.score = 15
        elif frame[1] == 'X':
            self.score = 20
        elif frame[1].isdigit():
            self.score = int(frame[1])


class ScoreHandler:

    def __init__(self, frames):
        self.frames = frames
        self.state_list = [FirstState(), SecondState()]
        self.state = None
        self.total_score = 0

    def switch_state(self):
        if self.state is None or isinstance(self.state, FirstState):
            self.state = self.state_list[1]
        else:
            self.state = self.state_list[0]

    def count_score(self):
        for frame in self.frames:
            self.switch_state()
            self.state.count(frame)
            if self.state.score in [15, 20]:
                self.total_score += self.state.score
                self.switch_state()
            else:
                self.total_score += self.state.score
                self.switch_state()
                self.state.count(frame)
                self.total_score += self.state.score
