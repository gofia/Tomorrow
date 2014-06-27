__author__ = 'lfi'

from numpy import exp

from sim_base import SimBase


class SimABS(SimBase):
    parameters = {
        'r': 0.001,
        'y': 1.0,
        'ps': 2.0,
        'v': 1.0,
        'g': 1.9,
        'a': 1.0,
        'o': 1.0,
        'b': 2.0,
        'n': 0.99,
        'alpha': 1800,
    }
    variables = {
        'n1': [0.5, 0.5],
        'n2': [0.5, 0.5],
        'p': [1.99, 2.01],
        'U1': [0.0, 0.0],
        'U2': [0.0, 0.0],
    }

    def update_p(self):
        return self.n1 * (self.ps + self.v * (self.p_1 - self.ps)) +\
            self.n2 * (self.p_1 + self.g * (self.p_1 - self.p_2)) +\
            self.y

    def update_U1(self):
        return (self.p_1 + self.y - (1 + self.r) * self.p_2) *\
            (self.ps + self.v * (self.p_1 - self.ps) + self.y - (1 + self.r) * self.p_2) /\
            (self.a * self.o) + self.n * self.U1_1

    def update_U2(self):
        return (self.p_1 + self.y - (1 + self.r) * self.p_2) *\
            (self.p_1 + self.g * (self.p_1 - self.p_2) + self.y - (1 + self.r) * self.p_2) /\
            (self.a * self.o) + self.n * self.U2_2

    def update_n1(self):
        Z = exp(self.b * self.U1_1) + exp(self.b * self.U2_1)
        nt2 = exp(self.b * self.U2_1) / Z
        return 1 - nt2 * exp(-(self.p_1 - self.ps) * (self.p_1 - self.ps) / self.alpha)

    def update_n2(self):
        Z = exp(self.b * self.U1_1) + exp(self.b * self.U2_1)
        nt2 = exp(self.b * self.U2_1) / Z
        return nt2 * exp(-(self.p_1 - self.ps) * (self.p_1 - self.ps) / self.alpha)


if __name__ == '__main__':
    print "Simulation start"
    sim = SimABS()
    print sim
    for i in range(0, 5):
        sim.run(1)
        print sim
    sim.plot("p")
