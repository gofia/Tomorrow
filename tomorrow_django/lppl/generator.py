__author__ = 'lucas.fievet'


class Generator():
    def __init__(self, function):
        self.func = function

    def generate(self, a, b, step):
        return [self.func(x) for x in range(a, b, step)]
