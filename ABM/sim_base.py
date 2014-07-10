__author__ = 'lfi'

import copy
import re
import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import skew, kurtosis


class SimBase(object):
    parameters = {}
    variables = {}

    def __getattr__(self, name, t=-1):
        m = re.search('(\S*)_(\d*)$', name)
        if m is not None:
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
            for keys in self.updates:
                new_values = {}
                for key in keys:
                    new_values[key] = self.__getattribute__("update_{0}".format(key))()
                for key in keys:
                    self.__setattr__(key, new_values[key])

    def run_until(self, name, upper=1E-3):
        old_value, new_value = 0.0, 1.0
        while abs(new_value - old_value) > upper:
            self.run(1000)
            old_value = new_value
            new_value = self.__getattribute__("diff_{0}".format(name))("p")
            # print "Change {0}: {1}.".format(name, new_value - old_value)
        return new_value

    def scan_parameter(self, parameter_name, values, property_name):
        initial_variables = copy.copy(self.variables)
        for value in values:
            self.variables = initial_variables
            self.__setattr__(parameter_name, value)
            property_value = self.run_until(property_name)
            print "{0}={1} => {2}={3}".format(parameter_name, value, property_name, property_value)

    def diff_method(self, name, method):
        array = np.array(self.variables[name])
        array_diff = np.diff(array)
        return method(array_diff)

    def diff_mean(self, name):
        return self.diff_method(name, np.mean)

    def diff_median(self, name):
        return self.diff_method(name, np.median)

    def diff_std(self, name):
        return self.diff_method(name, np.std)

    def diff_skewness(self, name):
        return self.diff_method(name, skew)

    def diff_kurtosis(self, name):
        return self.diff_method(name, kurtosis)

    def print_diff_information(self, name):
        print "----------"
        print "Variable {0}".format(name)
        print "----------"
        print "Mean: {0}".format(self.diff_mean(name))
        print "Median: {0}".format(self.diff_median(name))
        print "Standard: {0}".format(self.diff_std(name))
        print "Skewness: {0}".format(self.diff_skewness(name))
        print "Kurtosis: {0}".format(self.diff_kurtosis(name))

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

    def print_parameters(self):
        s = ""
        for key in self.parameters.keys():
            s += "{0}: {1}\n".format(key, self.__getattr__(key))
        print s

    def __str__(self):
        s = ""
        s += "\n"
        s += "----------\n"
        s += "Simulation\n"
        s += "----------\n"
        for key in self.variables.keys():
            s += "{0}: {1}\n".format(key, self.__getattr__(key))
        return s
