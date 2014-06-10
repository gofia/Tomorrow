__author__ = 'lfi'


class SimBase(object):
    parameters = []
    parameter_names = {}
    variables = []
    variable_names = {}

    def __getattr__(self, name):
        if name in self.variable_names and len(self.variables[self.variable_names[name]]) > 0:
            return self.variables[self.variable_names[name]][-1]
        if name in self.parameter_names:
            return self.parameters[self.parameter_names[name]]
        return super(SimBase, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name in self.variable_names:
            self.variables[self.variable_names[name]].append(value)
        if name in self.parameter_names:
            self.parameters[self.parameter_names[name]] = value
        return super(SimBase, self).__setattr__(name, value)

    def run(self, n):
        for key in self.variable_names.keys()