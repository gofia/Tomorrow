__author__ = 'lfi'

import re
import matplotlib.pyplot as plt


class SimBase(object):
    parameters = {}
    variables = {}

    def __getattr__(self, name, t=-1):
        m = re.search('(\S*)_(\d*)$', name)
        if not m is None:
            name = m.group(1)
            t = -int(m.group(2))
        if name in self.variables and len(self.variables[name]) > 0:
            return self.variables[name][t]
        if name in self.parameters:
            return self.parameters[name]
        return None

    def __setattr__(self, name, value):
        if name in self.variables:
            self.variables[name].append(value)
        if name in self.parameters:
            self.parameters[name] = value
        return super(SimBase, self).__setattr__(name, value)

    def run(self, n):
        for i in range(0, n):
            new_values = {}
            for key in self.variables.keys():
                new_values[key] = self.__getattribute__("update_{0}".format(key))()
            for key in self.variables.keys():
                self.__setattr__(key, new_values[key])

    def plot(self, *args):
        names = args[0:]
        fig = plt.figure(figsize=(16, 10))
        ax = fig.add_subplot(111)
        ax.set_xlabel("Time")
        ax.set_ylabel("Values")
        for name in names:
            if name in self.variables:
                ax.plot(self.variables[name])
        plt.show()

    def __str__(self):
        s = ""
        s += "\n"
        s += "----------\n"
        s += "Simulation\n"
        s += "----------\n"
        for key in self.parameters.keys():
            s += "{0}: {1}\n".format(key, self.__getattr__(key))
        for key in self.variables.keys():
            s += "{0}: {1}\n".format(key, self.__getattr__(key))
        return s
