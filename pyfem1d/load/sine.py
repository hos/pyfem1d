parameterValues = [25.,0.008]
parameterNames = ['loading_per','magnitude']

from math import sin,pi

def main(t):
    return parameterValues[1]*sin(t/parameterValues[0]*2.*pi)
