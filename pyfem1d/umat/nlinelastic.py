# Define all the constitutive relationships in this file
# --------------------------------------------------
#    Compute stress, modulus and update history
# --------------------------------------------------
from numpy import exp
parameterValues = [100,0.03]
parameterNames = ['elastic_mod','sat_rate']
#########################

def main(dt,n,eps):
    E   = parameterValues[0]
    eta = parameterValues[1]
    #Calculate the stress and consistent modulus
    sigl = E*eta*(1-exp(-1*eps/eta)) #nonlin elasticity
    aal = E*exp(-1*eps/eta)
    return sigl,aal



    #Update history
    #for j in range(nhist):
    #    h1[n,j] = hn[n][j] + dt*0.
