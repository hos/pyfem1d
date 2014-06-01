from __future__ import division, print_function, absolute_import

import __main__ as m

commands = ['ipShell', 'verbose', 'gui',
            'dt', 'nelem', 'tmax', 'bctype',
            'solve', 'help', 'plot', 'setLoading', 'setLoadingParameterValues',
            'setConstitutive', 'setConstitutiveParameterValues']


def ipShell():
    '''Start the interactive iPython shell with ipShell()'''
    m.an.execution.ipShell()

def verbose():
    '''Enable verbose output with verbose()'''
    m.an.execution.verbose = True

def gui():
    '''Start graphical user interface with gui()'''
    m.feminist.tkgui.startGui(m.an)

def dt(val):
    '''Set timestep size with dt(value)'''
    m.an.execution.dt = val

def nelem(val):
    '''Set total number of elements with nelem(value)'''
    m.an.execution.nelem = val

def tmax(val):
    '''Set maximum time tmax(value)'''
    m.an.execution.tmax = val

def bctype(val):
    '''Set bc type with bctype(val), can be 0,1,2'''
    m.an.execution.bctype = val

def solve():
    '''Start solution with solve()'''
    m.an.solve()

def plot(stressFile=None):
    '''Plot the output stress file using gnuplot. optional argument: stressFile'''
    m.an.execution.plotToWindow(stressFile=stressFile)

def plotPdf(stressFile=None, plotFile=None):
    '''Plot the output stress file to a pdf file using gnuplot. optional arguments: stressFile, plotFile'''
    m.an.execution.plotPdf(stressFile=stressFile, plotFile=plotFile)

def setLoading(val):
    '''Set loading function with setLoading(stringVal). example: setLoading('triangle')'''
    m.an.execution.load.setFunction(val)

def setConstitutive(val):
    '''Set constitutive function with setConstitutive(stringVal). example: setLoading('maxwell')'''
    m.an.execution.constitutive.setFunction(val)

def setConstitutiveParameterValues(val):
    '''Set constitutive function parameters with setConstitutiveParameterValues(array).
    example: setLoading([100,200,300])'''
    m.an.execution.constitutive.setParameterValues(val)

def setLoadingParameterValues(val):
    '''Set loading function parameters with setLoadingParameterValues(array).
    example: setLoading([100,200,300])'''
    m.an.execution.load.setParameterValues(val)

def help():
    '''Prints this help'''
    import feminist.ipython_wrappers as w
    #import pdb; pdb.set_trace()
    for i in commands:
        print(" >> %-10s : %s"%(i,w.__dict__[i].__doc__))
