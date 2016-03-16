parameterValues = [0,10,0.008]
parameterNames = ['start','end','magnitude']
from math import sin,pi

def main(t):
    if t<=parameterValues[1] and t>=parameterValues[0]:
        return parameterValues[2]
    else:
        return 0
