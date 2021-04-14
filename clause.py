from enum import Enum

class Operator(Enum):
    AND = 0,
    OR = 1,
    IMPLIES = 2


class Clause(object):

    def __init__(self, fluent=None):
        if fluent:
            self._clause = [fluent]
            self._single = True
        else:
            self._clause = []
            self._single = False

    def __repr__(self):
        return f"Clause object. {self._clause}"


    def __getitem__(self, item):
        return self._clause[item]

    def __contains__(self, item):
        return True if item in self._clause else False

    def __eq__(self, other):
        if self._single == other.is_single and self._clause == other.clause:
            return True
        else:
            return False

    def add(self, fluent, operator: Operator):
        if len(self._clause) == 0:
            self._single = True
        else:
            self._single = False
            self._clause.append(operator)
        self._clause.append(fluent)

        return self

    @property
    def clause(self):
        return self._clause

    @property
    def is_single(self):
        return self._single

    @property
    def empty(self):
        return self._clause == []