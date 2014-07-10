__author__ = 'lfi'

from numpy import exp, random, arange

from sim_base import SimBase


class SimABS(SimBase):
    parameters = {
        'r': 0.001,
        'y_avg': 1.0,
        'ps': 1000,
        'v': 0.9,
        'g': 1.9,
        'a': 1.0,
        'o': 1.0,
        'b': 2.0,
        'n': 0.99,
        'alpha': 1800,
        'noise': 25.0,
    }
    variables = {
        'n1': [],
        'n2': [],
        'p': [920, 920, 920],
        'U1': [0.0],
        'U2': [0.0],
        'y': [],
        'epsilon': [],
    }
    updates = [
        ["epsilon", "y", "n1", "n2"],
        ["p"],
        ["U1", "U2"],
    ]

    def update_epsilon(self):
        return random.normal(0, self.noise)

    def update_y(self):
        return random.normal(self.y_avg, self.o)

    def update_n1(self):
        return 1 - self.update_n2()

    def update_n2(self):
        nt2 = 1 / (exp(self.b * (self.U1 - self.U2)) + 1)
        return nt2 * exp(-(self.p - self.ps) * (self.p - self.ps) / self.alpha)

    def update_p(self):
        return self.n1 * (self.ps + self.v * (self.p - self.ps)) +\
            self.n2 * (self.p + self.g * (self.p - self.p_2)) +\
            self.y_avg + self.epsilon

    def update_U1(self):
        return (self.p + self.y - (1 + self.r) * self.p_2) *\
            (self.ps + self.v * (self.p_3 - self.ps) + self.y_avg - (1 + self.r) * self.p_2) /\
            (self.a * self.o * self.o) + self.n * self.U1

    def update_U2(self):
        return (self.p + self.y - (1 + self.r) * self.p_2) *\
            (self.p_3 + self.g * (self.p_3 - self.p_4) + self.y_avg - (1 + self.r) * self.p_2) /\
            (self.a * self.o * self.o) + self.n * self.U2


if __name__ == '__main__':
    print "Simulation start"
    sim = SimABS()
    sim.print_parameters()
    print sim
    sim.scan_parameter("v", arange(0.5, 1.01, 0.01), "std")
    # sim.run_until("std", 1E-4)
    # for i in range(0, 100000):
    #     sim.run(1)
        # print sim
    # sim.print_diff_information("p")
    # sim.plot("p")
