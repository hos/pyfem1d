import argparse
import os
import tempfile
import shutil
import atexit
import imp
import re
import ntpath
from subprocess import call
from numpy import zeros, dtype, float64
from pyfem1d.umat import *
from pyfem1d.load import *
import pyfem1d.umat_defaults
import pyfem1d.load_defaults


class Execution:
    def __init__(self):
        self.inputFile = None
        self.outputFile = None
        self.logFile = None
        self.stressFile = None
        self.displacementFile = None
        self.plotFile = None
        self.silent = False
        self.verbose = False
        self.interactive = False
        # self.gui = False
        self.o_node = None
        self.o_elem = None
        # self.umatDir = None
        # self.loadDir = None
        # self.umat = None
        self.umat_dict = {}
        self.load_dict = {}

        self.current_umat_key = None
        self.current_load_key = None

        self.umat = None
        self.load = None

        self.bctype = None
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.workingDirectory = None

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
        header += " Number of Elements    nelem = %i\n" % (self.mainpar.nelem)
        header += " Time step size           dt = %6.4f\n" % (self.mainpar.dt)
        header += " Duration               tmax = %6.4f\n" % (
            self.mainpar.tmax)
        header += " Boundary Condition   bctype = %i\n" % (self.mainpar.bctype)
        header += " Material model : %s\n" % (type(self.umat).__name__)
        # import pdb; pdb.set_trace()
        for i, j in zip(self.umat.parameter_names, self.umat.parameter_values):
            header += "  > " + str(i) + " : " + str(j) + "\n"
        header += " Loading function: %s\n" % (type(self.load).__name__)
        for i, j in zip(self.load.parameter_names, self.load.parameter_values):
            header += "  > " + str(i) + " : " + str(j) + "\n"
        return header

    def printHeader(self):
        '''Prints program header with version'''
        print("pyfem1d - 1d finite elements for testing material formulations")
        #print(self.getHeader())

    def test(self):
        self.inputFile = 'ASDADASD'

    def parseCmd(self):
        '''Parses command line'''
        self.abspath = os.path.dirname(os.path.abspath(__file__))

        parser = argparse.ArgumentParser()
        parser.add_argument('input',
                            metavar='input_file',
                            nargs='?',
                            help='input file',
                            type=argparse.FileType('r'))
        parser.add_argument('-o',
                            '--output-file',
                            default='default_out.dat',
                            type=argparse.FileType('w'))
        #parser.add_argument('-l', '--log-file', default='default.log',
        #type=argparse.FileType('w'))
        parser.add_argument('-d',
                            '--displacement-file',
                            default='default_disp.dat',
                            type=argparse.FileType('w'))
        parser.add_argument('-u',
                            '--stress-file',
                            default='default_stre.dat',
                            type=argparse.FileType('w'))
        parser.add_argument('-p',
                            '--plot-file',
                            default='default.ps',
                            type=argparse.FileType('w'))
        parser.add_argument('-n',
                            '--number-of-elements',
                            default='10',
                            type=int)
        parser.add_argument('-t', '--timestep', default='0.1', type=float)
        parser.add_argument('-m', '--maximum-time', default='25', type=float)
        # parser.add_argument('--umat-dir', default=os.path.join(self.abspath,'umat_temp'), type=is_dir, action=FullPaths)
        # parser.add_argument('--load-dir', default=os.path.join(self.abspath,'load_temp'), type=is_dir, action=FullPaths)
        # parser.add_argument('-g', '--gui', action='store_true', help='Start the graphical user interface')
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-s', '--silent', action='store_true')
        parser.add_argument('-i', '--interactive', action='store_true')
        args = parser.parse_args()

        #import pdb; pdb.set_trace()
        self.silent = args.silent
        self.verbose = args.verbose
        self.interactive = args.interactive
        # self.gui = args.gui

        # input file
        if args.input:
            self.inputFile = os.path.abspath(args.input.name)
            self.workingDirectory = os.path.dirname(os.path.abspath(
                args.input.name))
        else:
            self.workingDirectory = os.getcwd()

        self.outputFile = os.path.abspath(args.output_file.name)
        #self.logFile = os.path.abspath(args.log_file.name)
        self.stressFile = os.path.abspath(args.stress_file.name)
        self.displacementFile = os.path.abspath(args.displacement_file.name)
        self.plotFile = os.path.abspath(args.plot_file.name)

        self.add_umats(os.path.abspath(pyfem1d.umat_defaults.__file__))
        self.add_loads(os.path.abspath(pyfem1d.load_defaults.__file__))
        # import pdb; pdb.set_trace()

        # self.umatDir = args.umat_dir
        # self.loadDir = args.load_dir

        # self.umat = UserDefined(self.umatDir,self.abspath)
        # self.load = UserDefined(self.loadDir,self.abspath)

        #self.bctypelist = [0,1,2]
        self.p0 = ['nelem', 'dt', 'tmax', 'bctype']
        self.p1 = [args.number_of_elements, args.timestep, args.maximum_time,
                   [0, 1, 2]]
        #self.p1 = [self.nelem,self.dt,self.tmax,self.bctypelist]
        self.p2 = ['# of the elements', 'Timestep', 'Max time', 'BC TYPE']

        self.mainpar = ParameterList()
        for i, j, k in zip(self.p0, self.p1, self.p2):
            self.mainpar.addvar(i, j, metavar=k)

        self.mainpar.setOptions('bctype', [
            "0 - Clamped bar subjected to a single force at the free end - Stress controlled",
            "1 - Clamped bar with uniform body load - Stress controlled",
            "2 - Clamped bar subjected to displacement-driven loading at the free end - Strain controlled"
        ])

    def add_umats(self, path):
        self.umat_dict.update(deploy_umats(path))

    def add_loads(self, path):
        self.load_dict.update(deploy_loads(path))

    def set_umat(self, key):
        self.umat = self.umat_dict[key]()
        self.current_umat_key = key

    def set_umat_parameters(self, parameters):
        self.umat.parameter_values = parameters
        self.umat_dict[self.current_umat_key].parameter_values = parameters

    def set_load(self, key):
        self.load = self.load_dict[key]()
        self.current_load_key = key

    def set_load_parameters(self, parameters):
        self.load.parameter_values = parameters
        self.load_dict[self.current_load_key].parameter_values = parameters

    # IPython Stuff

    #def ipShellWithNamespace(self,ns):
    #'''Starts the interactive IPython shell'''
    #from IPython import embed
    #from IPython.config.loader import Config
    #cfg = Config()
    #cfg.TerminalInteractiveShell.confirm_exit = False
    #embed(config = cfg, user_ns = ns, display_banner = False)

    #def ipShell(self):
    #'''Starts the interactive IPython shell
    #namespace defaults to __main__.__dict__'''
    #from __main__ import __dict__ as ns
    #self.ipShellWithNamespace(ns)

    def update(self):
        try:
            self.const_main = self.umat.main()
        except:
            print("Error: No main function defined in the material.")
            raise
        try:
            self.const_initcond = self.umat.initcont()
        except:
            self.const_initcond = False
        try:
            self.const_update = self.umat.update()
        except:
            self.const_update = False

    def plotToWindow(self, stressFile=None):
        if not stressFile:
            stressFile = self.stressFile
        commands = ""
        commands += "set terminal X11 size 1300 400;"
        commands += "set key rmargin;"
        commands += "set multiplot;"
        commands += "set lmargin at screen 0.025;"
        commands += "set rmargin at screen 0.325;"
        commands += "set xlabel 'Time';"
        commands += "set ylabel 'Strain';"
        commands += "plot \'%s\' u 1:2 w l;" % stressFile
        commands += "set lmargin at screen 0.35;"
        commands += "set rmargin at screen 0.65;"
        commands += "set ylabel 'Stress';"
        commands += "plot \'%s\' u 1:3 w l;" % stressFile
        commands += "set lmargin at screen 0.675;"
        commands += "set rmargin at screen 0.975;"
        commands += "set xlabel 'Strain';"
        commands += "plot \'%s\' u 2:3 w l;" % stressFile
        commands += "unset multiplot;"

        call(["gnuplot", "-p", "-e", commands])

#set output '| ps2pdf -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress - '''+self.ofilebase+'''_plot.pdf;\

    def plotPdf(self, stressFile=None, plotFile=None):
        if not stressFile:
            stressFile = self.stressFile

        if not plotFile:
            plotFile = self.plotFile

        if not self.silent:
            print('Plotting to file %s' % plotFile)

        commands = ""
        commands += "set term postscript landscape enhanced color;"
        commands += "set output \'%s\';" % plotFile
        commands += "set lmargin;"
        commands += "set rmargin;"
        commands += "set xlabel \'Time\';"
        commands += "set ylabel \'Strain\';"
        commands += "plot \'%s\' u 1:2 w l lw 3 lt 1;" % stressFile
        commands += "set ylabel \'Stress\';"
        commands += "plot \'%s\' u 1:3 w l lw 3 lt 1;" % stressFile
        commands += "set xlabel \'Strain\';"
        commands += "plot \'%s\' u 2:3 w l lw 3 lt 1;" % stressFile

        call(["gnuplot", "-p", "-e", commands])


class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest,
                os.path.abspath(os.path.expanduser(values)))


def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


def getModuleName(moduleFilePath):
    '''Gets the module name from arbitrary paths, like
    /a/b/module.py, module.py, module, a/module.py'''
    moduleBasename = ntpath.basename(moduleFilePath)
    if moduleBasename[-3:] == '.py':
        moduleBasename = moduleBasename[:-3]

    return moduleBasename


class parameter:
    def __init__(self, variable, metavar=None, options=None):
        self.variable = variable
        self.metavar = metavar
        self.options = options

    def setOptions(self, options):
        self.options = options

    def setMetavar(self, metavar):
        self.metavar = metavar


class ParameterList:
    def __init__(self):
        self.parameters = []

    def updatesize(self):
        self.size = len(self.parameters)

    def addvar(self, variable, value, options=[], metavar=[]):
        self.__dict__[variable] = value
        self.parameters.append(parameter(variable,
                                         metavar=metavar,
                                         options=options))
        self.updatesize()

    def parseArguments(self, *args):
        if len(args) > 2:
            print("Error: Invalid number of arguments")
            raise Exception
        parameters = []
        values = []
        dummy = []

        for i in args:
            dummy.append(i)

        if len(dummy) >= 1:
            parameters = dummy[0]
            if len(dummy) == 2:
                values = dummy[1]
        return parameters, values

    def getMetavars(self):
        a = []
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
        if len(parameters) != self.size:
            print("Error: 'parlist' lengths do not match", parameters)
            return
        for i, j in zip(self.parameters, parameters):
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
        raise Exception("Error: could not find opt: %s" % (parameters))
