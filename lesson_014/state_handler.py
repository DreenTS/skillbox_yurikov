from abc import ABC, abstractmethod


class State(ABC):

    def __init__(self, is_spare=False, is_strike=False):
        self.res = 0
        self.is_spare = is_spare
        self.is_strike = is_strike

    @abstractmethod
    def private_count(self, char):
        pass

    @abstractmethod
    def public_count(self, char):
        pass


class FirstThrow(State):

    def private_count(self, char):
        self.res = int(char)
        return SecondThrow(), self.res

    def public_count(self, char):
        if self.is_spare:
            self.is_spare = False
            self.res = int(char)
            return self, self.res
        if self.is_strike:
            self.is_strike = False
        self.res = int(char)
        return SecondThrow(is_spare=self.is_spare, is_strike=self.is_strike), self.res


class SecondThrow(State):

    def private_count(self, char):
        if char == 'X':
            self.res = 20
        elif char == '/':
            self.res = 15
        else:
            self.res = int(char)
        return FirstThrow(), self.res

    def public_count(self, char):
        if char == '/':
            self.res = 10
            self.is_spare = True
        elif char == 'X':
            self.res = 10
            self.is_strike = True
        else:
            self.res = int(char)
        return FirstThrow(is_spare=self.is_spare, is_strike=self.is_strike), self.res


class ScoreHandler:

    def __init__(self, result, mode):
        self.result = result
        self.mode = mode
        self.state = None
        self.total_score = 0

    def count_score(self):
        self.state, prev, curr, local_state = FirstThrow(), 0, 0, None
        if self.mode == 'private':
            for char in self.result:
                self.state, curr = self.state.private_count(char=char)
                if curr in [15, 20]:
                    self.total_score += curr - prev
                else:
                    self.total_score += curr
                prev = curr
        else:
            for i in range(len(self.result)):
                if i == 18 and ('X' in self.result[i:i+2] or '/' in self.result[i:i + 2]):
                    self.total_score += 10
                    break
                else:
                    self.state, curr = self.state.public_count(char=self.result[i])
                    if self.state.is_spare:
                        self.state, curr = self.state.public_count(char=self.result[i + 1])
                        self.total_score += curr + 10 - prev
                        self.state.res = 0
                    elif self.state.is_strike:
                        local_state = self.state
                        self.total_score += curr
                        self.state, prev = self.state.public_count(char=self.result[i + 1])
                        self.state, curr = self.state.public_count(char=self.result[i + 2])
                        if self.state.is_spare or self.state.is_strike:
                            self.total_score += 10
                            if self.state.is_strike:
                                self.state, curr = self.state.public_count(char=self.result[i + 3])
                                self.total_score += curr
                        else:
                            self.total_score += prev + curr
                        self.state = local_state
                    else:
                        self.total_score += curr
                        prev = curr
