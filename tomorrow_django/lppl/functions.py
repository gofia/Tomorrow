__author__ = 'lucas.fievet'


from numpy.core.umath import cos, log
from abc import abstractmethod


class Function():
    @abstractmethod
    def value(self, t):
        pass

    class Meta:
        abstract = True


class lppl(Function):
    def __init__(self, A, B, m, t_0, omega, phi):
        self.A = A
        self.B = B
        self.m = m
        self.t_0 = t_0
        self.omega = omega
        self.phi = phi

    def value(self, t):
        return self.A + self.B * (1 / (t - self.t_0) ** self.m +
                                  cos(self.omega * log(t - self.t_0) + self.phi))
