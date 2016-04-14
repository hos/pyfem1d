import numpy as np

#default values and parameter names
parameterValues = [100,1500]
parameterNames = ['elastic_mod','viscosity']
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
    E   = parameterValues[0]
    eta = parameterValues[1]
    alphan=hn[n]
    #Calculate the stress and consistent modulus
    alpha=(alphan+eps*dt*E/eta)/(1+dt*E/eta)
    sigl = E*(eps-alpha)
    aal =  E/(1+dt*E/eta)

    h1[n]=alpha

    return sigl,aal
