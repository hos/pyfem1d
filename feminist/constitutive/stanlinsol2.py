from numpy import *

parameterValues = [1000,4000,20000]
parameterNames = ['E0','E1','viscosity']

tol=1e-10

h1=[];hn=[]
#########################
def initcond(asdf):
    global h1,hn,nelem
    h1=zeros((asdf,1),dtype=float64)
    hn=zeros((asdf,1),dtype=float64)
    nelem=asdf

def update():
    global h1,hn
    temp=h1[:]
    h1=hn[:]
    hn=temp[:]

#########################################
#####    CONSTITUTIVE EQUATIONS    ######
#########################################
def sigel1(strain):#elastic stress
    result=strain*parameterValues[1]
    return result

def sigel0(strain):#elastic stress
    result=strain*parameterValues[0]
    return result

def epsvisdot(stress):# viscous strain derivative
    result=stress/parameterValues[2]
    return result

def sig(eps,alpha): #total stress
    result=sigel0(eps) + sigel1(eps-alpha)
    return result

#########################################
#####    SECANT ITERATION          ######
#########################################

offset=0.1
def nextstep(hist,dt,eps):
    trolo=[hist-offset,hist]
    #using the secant method
    #print '     ++++++++++++++++'
    while True:
        temp2=trolo[1]-residual(trolo[1],hist,dt,eps) * (trolo[1]-trolo[0]) / (residual(trolo[1],hist,dt,eps)-residual(trolo[0],hist,dt,eps))
        trolo[0]=trolo[1]
        trolo[1]=temp2
        err=abs(trolo[0]-trolo[1])

        #print '     >>>>> Secant_err: %10.5e' %(err)
        if err<tol: break
    return trolo[1]

# RESIDUAL
def residual(sonra,simdi,dt,eps):
    result=sonra-simdi-dt*epsvisdot(sigel1(eps-sonra))
    return result

#########################################
#####    FIVE POINT STENCIL        ######
#########################################

#step size for the five-point stencil
fs=0.001

#def fivepoint(f,*p):
    #return (-1*f(p[0]+2*fs,p[1:])+8*f(p[0]+fs,p[1:])-8*f(p[0]-fs,p[1:])+f(p[0]-2*fs,p[1:]))/(12*fs)


#########################################
#####         MAIN FUNCTION        ######
#########################################

def main(dt,n,eps):
    global h1,hn,nelem

    alphan=hn[n]

    #CALCULATE THE NEXT VISCOUS STRAIN
    alpha=nextstep(alphan,dt,eps)

    #calculate the stress and the consistent modulus
    sigl = sig(eps,alpha)
    #aal  = fivepoint(sig,eps,alpha)
    aal  = (-1*sig(eps+2*fs,alpha)+8*sig(eps+fs,alpha)-8*sig(eps-fs,alpha)+sig(eps-2*fs,alpha))/(12*fs)
    #Update history
    h1[n]=alpha

    return sigl,aal
