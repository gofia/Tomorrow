__author__ = 'lfi'

from numpy import exp

from sim_base import SimBase


class SimABS(SimBase):
    parameters = {
        'r': 0.05,
        'y': 0.1,
        'ps': 2,
        'v': 0.1,
        'g': 0.1,
        'a': 1.0,
        'o': 1.0,
        'b': 0.5,
        'n': 0.5,
        'alpha': 0.5,
    }
    variable = {
        'n1': [0.5, 0.5],
        'n2': [0.5, 0.5],
        'p': [1.0, 1.0],
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
    for i in range(0, 50):
        sim.run(1)
    sim.plot("p")
