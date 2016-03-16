import numpy as np

#default values and parameter names
parameterValues = [1000,4000,20000]
parameterNames = ['E0','E1','viscosity']
h1=[];hn=[]

def initcond(asdf):
    global h1,hn,nelem
    h1=np.zeros((asdf,1),dtype=np.float64)
    hn=np.zeros((asdf,1),dtype=np.float64)
    nelem=asdf

def update():
    global h1,hn
    temp=h1[:]
    h1=hn[:]
    hn=temp[:]

def main(dt,n,eps):
    global h1,hn,nelem
    #Get the material variables
    E0   = parameterValues[0]
    E1   = parameterValues[1]
    eta = parameterValues[2]
    alphan=hn[n]

    #Calculate the stress and consistent modulus
    alpha=(alphan+eps*dt*E1/eta)/(1+dt*E1/eta)

    sigl = E0*eps + E1*(eps-alpha)
    aal  = E0 + E1/(1+dt*E1/eta)#
    #Update history
    h1[n]=alpha

    return sigl,aal
