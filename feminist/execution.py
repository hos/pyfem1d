from __future__ import division, print_function, absolute_import

import argparse
import os
import tempfile
import shutil
import atexit
import imp
import re
from numpy import zeros,dtype,float64

class Execution:
    def __init__(self):
        self.inputFile = None
        self.outputFile = None
        self.logFile = None
        self.stressFile = None
        self.displacementFile = None
        self.silent = False
        self.verbose = False
        self.interactive = False
        self.gui = False
        self.o_node = None
        self.o_elem = None
        self.constitutiveDir = None
        self.loadDir = None
        self.constitutive = None
        self.load = None
        self.bctype = None
        self.abspath = os.path.dirname(os.path.abspath(__file__))

    def getHeader(self):
        header = ""
        if self.inputFile:
            header += " Input file   : " + self.inputFile + "\n"
        else:
            header += " Input file   : None\n"

        header += " Output file  : " + self.outputFile + "\n"
        header += " Stress file  : " + self.stressFile + "\n"
        header += " Disp. file   : " + self.displacementFile + "\n"
        #header += " Log file     : " + self.logFile + "\n"
        header += " The following parameters have been set:\n"
        header += " Number of Elements    nelem = %i\n" %(self.mainpar.nelem)
        header += " Time step size           dt = %6.4f\n"%(self.mainpar.dt)
        header += " Duration               tmax = %6.4f\n"%(self.mainpar.tmax)
        header += " Boundary Condition   bctype = %i\n"%(self.mainpar.bctype)
        header += " Material model : %s\n"%(self.constitutive.function)
        for i,j in zip(self.constitutive.getMetavars(), self.constitutive.getParameterValues()):
            header += "  > " + str(i) + " : " + str(j) + "\n"
        header += " Loading function: %s\n"%(self.load.function)
        for i,j in zip(self.load.getMetavars(), self.load.getParameterValues()):
            header += "  > " + str(i) + " : " + str(j) + "\n"
        return header


    def printHeader(self):
        '''Prints program header with version'''
        print("feminist - 1d finite elements for testing material formulations")
        #print(self.getHeader())

    def test(self):
        self.inputFile = 'ASDADASD'

    def parseCmd(self):
        '''Parses command line'''
        self.abspath = os.path.dirname(os.path.abspath(__file__))

        parser = argparse.ArgumentParser()
        parser.add_argument('input', metavar='input_file', nargs='?',
                            help='input file',
                            type=argparse.FileType('r'))
        parser.add_argument('-o', '--output-file', default='default_out.dat',
                            type=argparse.FileType('w'))
        #parser.add_argument('-l', '--log-file', default='default.log',
                            #type=argparse.FileType('w'))
        parser.add_argument('-d', '--displacement-file', default='default_disp.dat',
                            type=argparse.FileType('w'))
        parser.add_argument('-p', '--stress-file', default='default_stre.dat',
                            type=argparse.FileType('w'))
        parser.add_argument('-n', '--number-of-elements', default='10', type=int)
        parser.add_argument('-t', '--timestep', default='0.1', type=float)
        parser.add_argument('-m', '--maximum-time', default='25', type=float)
        parser.add_argument('--constitutive-dir', default=os.path.join(self.abspath,'constitutive'), type=is_dir, action=FullPaths)
        parser.add_argument('--load-dir', default=os.path.join(self.abspath,'load'), type=is_dir, action=FullPaths)
        parser.add_argument('-g', '--gui', action='store_true', help='Start the graphical user interface')
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-s', '--silent', action='store_true')
        parser.add_argument('-i', '--interactive', action='store_true')
        args = parser.parse_args()

        #import pdb; pdb.set_trace()
        self.silent = args.silent
        self.verbose = args.verbose
        self.interactive = args.interactive
        self.gui = args.gui

        # input file
        if args.input:
            self.inputFile = os.path.abspath(args.input.name)

        self.outputFile = os.path.abspath(args.output_file.name)
        #self.logFile = os.path.abspath(args.log_file.name)
        self.stressFile = os.path.abspath(args.stress_file.name)
        self.displacementFile = os.path.abspath(args.displacement_file.name)

        #import pdb; pdb.set_trace()
        self.constitutiveDir = args.constitutive_dir
        self.loadDir = args.load_dir

        self.constitutive = UserDefined(self.constitutiveDir,self.abspath)
        self.load = UserDefined(self.loadDir,self.abspath)

        #self.bctypelist = [0,1,2]
        self.p0 = ['nelem','dt','tmax','bctype']
        self.p1 = [args.number_of_elements, args.timestep, args.maximum_time, [0,1,2]]
        #self.p1 = [self.nelem,self.dt,self.tmax,self.bctypelist]
        self.p2 = ['# of the elements','Timestep','Max time','BC TYPE']

        self.mainpar = ParameterList()
        for i, j, k in zip(self.p0, self.p1, self.p2):
            self.mainpar.addvar(i, j, metavar = k)

        self.mainpar.setOptions('bctype',["0 - Clamped bar subjected to a single force at the free end - Stress controlled","1 - Clamped bar with uniform body load - Stress controlled","2 - Clamped bar subjected to displacement-driven loading at the free end - Strain controlled"])

    # IPython Stuff

    def ipShellWithNamespace(self,ns):
        '''Starts the interactive IPython shell'''
        from IPython import embed
        from IPython.config.loader import Config
        cfg = Config()
        cfg.TerminalInteractiveShell.confirm_exit = False
        embed(config = cfg, user_ns = ns, display_banner = False)

    def ipShell(self):
        '''Starts the interactive IPython shell
        namespace defaults to __main__.__dict__'''
        from __main__ import __dict__ as ns
        self.ipShellWithNamespace(ns)

    def update(self):
        try:
            self.const_main = self.constitutive.main()
        except:
            print("Error: No main function defined in the material.")
            raise
        try:
            self.const_initcond = self.constitutive.initcont()
        except:
            self.const_initcond = False
        try:
            self.const_update = self.constitutive.update()
        except:
            self.const_update = False


class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))

def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname

#Class for the user defined functions under directories

class UserDefined:
    def __init__(self, direc, abspath):
        #enable the defined functions in the class's namespace:
        #self.setFunction=self.setFunction

        #self.gett=self.gett
        #self.sett=self.sett

        self.modname=direc
        self.listt=[]
        self.imp = {}
        for module in os.listdir(direc):
            if module == '__init__.py' or module[-3:] != '.py':
                continue
            submodule = module[:-3]
            #print submodule
            self.imp[submodule] = imp.load_source(submodule,os.path.join(direc,module))
            #__import__(abspath+'/'+direc+'.'+module[:-3])
            #__import__(direc+'.'+module[:-3])
            self.listt.append(submodule)
        #print vars(self.imp)
        if self.listt==[]:
            print("Error: No valid function found in the directory:"+ self.modname)
            self.__delete__()
        self.setDefaultIndex(0)

    def setFunction(self,function):
        valid=False
        for i in self.listt:
            if i==function:
                valid=True
                break
        if valid==False:
            print("Error: Invalid default string assignment")
        a = self.imp[function]

        if not a.parameterValues:
            raise Exception("Module "+a.__name__+" parameterValues is not defined")

        if not a.parameterNames:
            raise Exception("Module "+a.__name__+": parameterNames is not defined")

        if len(a.parameterValues) != len(a.parameterNames):
            raise Exception("Module "+a.__name__+": len(parameterValues) != len(parameterNames)")
        self.size = len(a.parameterValues)
        self.function = function


    def main(self):
        return vars(self.imp[self.function])['main']

    def initcond(self):
        try:
            return vars(self.imp[self.function])['initcond']
        except:
            return
    def update(self):
        try:
            return vars(self.imp[self.function])['update']
        except:
            return

    def setDefaultIndex(self,ind):
        if ind>len(self.listt):
            print("Error: Invalid default index assignment")
        self.defaultind=ind
        self.setFunction(self.listt[self.defaultind])

    def parseArguments(self, *args):
        if len(args)>2:
            print("Error: Invalid number of arguments")
            raise Exception
        parameters = []; values = []; dummy = []

        for i in args:
            dummy.append(i)

        if len(dummy) >= 1:
            parameters = dummy[0]
            if len(dummy) == 2:
                values = dummy[1]
        return parameters,values

    def getParameterValues(self):
        return vars(self.imp[self.function])['parameterValues']

    def getMetavars(self):
        return getattr(self.imp[self.function],'parameterNames')

    #def getOptions(self):
        #pass

    def setParameterValues(self, *args):
        from collections import Iterable
        parameters, values = self.parseArguments(*args)
        if (len(parameters) != len(vars(self.imp[self.function])['parameterValues']))\
                or not isinstance(parameters, Iterable):
            raise Exception(str(parameters)+": number of parameters does not match the material model")

        vars(self.imp[self.function])['parameterValues'] = parameters

    #def setParameter(self):
        #pass

    #def setOptions(self):
        #pass

class parameter:

    def __init__(self,variable,metavar = None, options = None):
        self.variable = variable
        #if metavar:
        self.metavar=metavar
        #if options:
        self.options=options

    def setOptions(self,options):
        self.options=options
    def setMetavar(self,metavar):
        self.metavar=metavar

class ParameterList:


    def __init__(self):
        self.parameters = []

    def updatesize(self):
        self.size=len(self.parameters)

    def addvar(self, variable, value, options = [], metavar = []):
        self.__dict__[variable] = value
        self.parameters.append(parameter(variable, metavar = metavar, options = options))
        self.updatesize()


    def parseArguments(self, *args):
        if len(args)>2:
            print("Error: Invalid number of arguments")
            raise Exception
        parameters = []; values = []; dummy = []

        for i in args:
            dummy.append(i)

        if len(dummy) >= 1:
            parameters = dummy[0]
            if len(dummy) == 2:
                values = dummy[1]
        return parameters,values

    def getMetavars(self):
        a=[]
        for i in self.parameters:
            a.append(i.metavar)
        return a



    #def getParameterList(self):
        #pass

    #def getParameter(self):
        #pass

    #def getOptions(self):
        #pass

    def getParameterValues(self):
        a = []
        for i in self.parameters:
            a.append(self.__dict__[i.variable])
        return a


    def setParameterValues(self, *args):
        parameters, values = self.parseArguments(*args)
        if len(parameters)!= self.size:
            print("Error: 'parlist' lengths do not match",parameters)
            return
        for i,j in zip(self.parameters,parameters):
            self.__dict__[i.variable] = j

    #def setParameters(self):
        #parameters, values = parseArguments(*args)
        #for i in self.par:
            #if i.name == name:
                #i.pars = val
                #return
        #print("Error: could not find pars: %s" %(par))

    def setOptions(self, *args):
        parameters, values = self.parseArguments(*args)
        for i in self.parameters:
            if i.variable == parameters:
                i.setOptions(values)
                return
        raise Exception("Error: could not find opt: %s" %(parameters))

