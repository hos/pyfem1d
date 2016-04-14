from math import sin, pi


class ExampleLoad(Load):
    parameter_values = [25., 0.008]
    parameter_names = ['loading_per', 'magnitude']

    def value(self, t):
        return self.parameter_values[1] * sin(t / self.parameter_values[0] *
                                              2. * pi)
