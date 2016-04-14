# Define all the constitutive relationships in this file
# --------------------------------------------------
#    Compute stress, modulus and update history
# --------------------------------------------------
parameterValues = [100]
parameterNames = ['elastic_mod']

def main(dt,n,eps):
    #Get the material variables
    #print parameterValues
    E   = parameterValues[0]
    #Calculate the stress and consistent modulus
    sigl = E*eps #linear elasticity
    aal = E
    return sigl,aal
