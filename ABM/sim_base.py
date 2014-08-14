__author__ = 'lfi'

import json
import hashlib
import copy
import re
import os
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import skew, kurtosis


class SimBase(object):
    name = "simulation"
    parameters = {}
    variables = {}
    scans = {}

    def __init__(self):
        self.initial_variables = copy.copy(self.variables)

    def reset_variables(self):
        self.variables = copy.copy(self.initial_variables)

    def compute_hash(self, parameters, initial_variables=None):
        if initial_variables is None:
            initial_variables = self.initial_variables
        h = self.name + json.dumps(parameters) + json.dumps(initial_variables)
        m = hashlib.sha224(h)
        return m.hexdigest()

    @property
    def hash(self):
        return self.compute_hash(self.parameters, self.initial_variables)

    @staticmethod
    def underscore_split(s):
        one, two = s, None
        m = re.search('(\S*)_(\d*)$', s)
        if m is not None:
            one = m.group(1)
            two = m.group(2)
        return one, two

    def __getattr__(self, name, t=-1):
        name, t = self.underscore_split(name)
        t = -1 if t is None else -int(t)
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

    def run_until(self, property, upper=1E-3):
        p_variable, p_name = property['variables'], property['name']
        old_value, new_value = 0.0, 1.0
        while abs(new_value - old_value) > upper:
            self.run(1000)
            old_value = new_value
            new_value = self.__getattribute__(p_name)(*p_variable)
        return new_value

    def scan_parameters(self, parameters, properties, scan=None):
        if not isinstance(parameters, list) or len(parameters) == 0:
            raise "Parameters need to be a list with at least one item"

        if not "name" in parameters[0] or not "values" in parameters[0]:
            raise "Parameter needs a name and values attribute."

        cache_file_hash = self.compute_hash(parameters)
        cache_file = "{0}.txt".format(cache_file_hash)
        if os.path.isfile(cache_file):
            f = open(cache_file, 'r')
            self.scans = json.loads(f.read())
            f.close()
            return -1

        # Pop first parameter
        first = False
        name = parameters[0]["name"]
        values = parameters[0]["values"]
        parameters = parameters[1:]
        print parameters

        # If no scan, use self
        if scan is None:
            first = True
            scan = self.scans

        if not name in scan:
            scan[name] = {'values': []}

        property_until = properties[0]
        count = 0

        for value in values:
            print "{0}: {1}".format(name, value)
            self.reset_variables()
            self.__setattr__(name, value)
            self.run_until(property_until)
            if len(parameters) == 0:
                count += 1
                scan[name]["values"].append(value)
                for p in properties:
                    p_variable, p_name = p['variables'], p['name']
                    full_name = "{0}_{1}".format("_".join(p_variable), p_name)
                    if full_name not in scan[name]:
                        scan[name][full_name] = {'values': []}
                    p_value = self.__getattribute__(p_name)(*p_variable)
                    print "{0}: {1}".format(full_name, p_value)
                    scan[name][full_name]['values'].append(p_value)
            else:
                last_count = self.scan_parameters(parameters, properties, scan[name])
                for _ in range(0, last_count):
                    scan[name]["values"].append(value)
                count += last_count

        if first:
            f = open(cache_file, 'w')
            f.write(json.dumps(self.scans))
            f.close()

        return count

    def plot_scan(self, *args):
        xs = []
        scan = self.scans
        for arg in args:
            xs.append(scan[arg]["values"])
            scan = scan[arg]

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.scatter(xs[0], xs[1], xs[2], color="red")
        ax.set_xlabel(args[0])
        ax.set_ylabel(args[1])
        ax.set_zlabel(args[2])
        plt.show()

    def mean(self, name):
        return np.mean(self.variables[name])

    def diff_correlate(self, name1, name2):
        array1 = np.array(self.variables[name1])
        array1_diff = np.diff(array1)
        array2 = np.array(self.variables[name2])
        array2_diff = np.diff(array2)
        return np.correlate(array1_diff, array2_diff)[0]

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
