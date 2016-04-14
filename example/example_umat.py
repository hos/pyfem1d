import numpy as np

class ExampleUmat(Umat):

    parameter_values = [100, 1500]
    parameter_names = ['elastic_mod', 'viscosity']

    def __init__(self):
        self.h1 = []
        self.hn = []

    def initial_cond(self, asdf):
        self.h1 = np.zeros((asdf, 1), dtype=np.float64)
        self.hn = np.zeros((asdf, 1), dtype=np.float64)
        self.nelem = asdf

    def update(self):
        temp = self.h1[:]
        self.h1 = self.hn[:]
        self.hn = temp[:]

    def stress_tangent(self, dt, n, eps):
        #Get the material variables
        E = self.parameter_values[0]
        eta = self.parameter_values[1]
        alphan = self.hn[n]
        #Calculate the stress and consistent modulus
        alpha = (alphan + eps * dt * E / eta) / (1 + dt * E / eta)
        sigl = E * (eps - alpha)
        aal = E / (1 + dt * E / eta)

        self.h1[n] = alpha

        return sigl, aal
