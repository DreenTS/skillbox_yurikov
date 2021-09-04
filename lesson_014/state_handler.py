from abc import ABC, abstractmethod


class State(ABC):

    def __init__(self, is_spare=False, is_strike=False):
        self.res = 0
        self.is_spare = is_spare
        self.is_strike = is_strike

    @abstractmethod
    def count(self, result):
        pass


class PrivateFirstThrow(State):

    def count(self, result):
        self.res = int(result)
        return self.res


class PrivateSecondThrow(State):

    def count(self, result):
        if result == 'X':
            self.res = 20
        elif result == '/':
            self.res = 15
        else:
            self.res = int(result)
        return self.res


class PublicFirstThrow(State):

    def count(self, result):
        if self.is_strike:
            self.is_strike = False
            local_state = PublicSecondThrow()
            local_state.count(result=result[1])
            if local_state.is_spare:
                self.res = local_state.res
                return self.res
            elif local_state.is_strike:
                self.res = local_state.res + self.count(result=result[2])
                return self.res
            else:
                self.res = int(result[0]) + local_state.res
                return self.res
        else:
            self.res = int(result)
            return self.res


class PublicSecondThrow(State):

    def count(self, result):
        if result == '/':
            self.is_spare = True
            self.res = 10
            return self.res
        elif result == 'X':
            self.is_strike = True
            self.res = 10
            return self.res
        else:
            self.res = int(result)
            return self.res


class ScoreHandler:

    def __init__(self, result, mode):
        self.result = result
        self.mode = mode
        self.state = None
        self.states_dict = {
            'private': (PrivateFirstThrow, PrivateSecondThrow),
            'public': (PublicFirstThrow, PublicSecondThrow)
        }
        self.total_score = 0

    def count_score(self):
        prev, curr, local_state = 0, 0, None
        # TODO self._switch_state повторяется в обоих ветках условного оператора, вызовите его один раз тут
        if self.mode == 'private':
            self._switch_state()
            for char in self.result:
                curr = self.state.count(result=char)
                if curr in [15, 20]:
                    self.total_score += curr - prev
                else:
                    self.total_score += curr
                self._switch_state()  # TODO кроме этого вызова, этот остаётся
                prev = curr
        else:
            self._switch_state()
            for i in range(len(self.result)):
                if i == 18 and ('X' in self.result[i:i + 2] or '/' in self.result[i:i + 2]):
                    self.total_score += 10
                    break
                else:
                    curr = self.state.count(result=self.result[i])
                    # TODO аналогично и ниже - повторяется вызов того же метода в начале каждой ветки
                    if self.state.is_spare:
                        self._switch_state()
                        self.total_score += curr - prev + self.state.count(result=self.result[i + 1])
                    elif self.state.is_strike:
                        self._switch_state()
                        self.state.is_strike = True
                        self.total_score += curr - prev
                        curr = self.state.count(result=self.result[i + 1: i + 4])
                        self.total_score += curr
                    else:
                        self.total_score += curr
                        self._switch_state()
                    prev = curr

    def _switch_state(self):
        if self.state is None:
            self.state = self.states_dict[self.mode][0]()
        elif isinstance(self.state, self.states_dict[self.mode][0]):
            self.state = self.states_dict[self.mode][1]()
        else:
            self.state = self.states_dict[self.mode][0]()
