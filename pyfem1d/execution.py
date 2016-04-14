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
        self.interactive = False
        # self.gui = False
        self.o_node = None
        self.o_elem = None

        self.umat_dict = {}
        self.load_dict = {}

        self.current_umat_key = None
        self.current_load_key = None

        self.umat = None
        self.load = None

        self.bctype = None
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.workingDirectory = None

        self.number_of_elements = None
        self.timestep = None
        self.maximum_time = None


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
        header += " Number of Elements    nelem = %i\n" % (self.number_of_elements)
        header += " Time step size           dt = %6.4f\n" % (self.timestep)
        header += " Duration               tmax = %6.4f\n" % (self.maximum_time)
        header += " Boundary Condition   bctype = %i\n" % (self.bctype)

        if self.umat:
            header += " Material model : %s\n" % (type(self.umat).__name__)
            for i, j in zip(self.umat.parameter_names, self.umat.parameter_values):
                header += "  > " + str(i) + " : " + str(j) + "\n"
        if self.load:
            header += " Loading function: %s\n" % (type(self.load).__name__)
            for i, j in zip(self.load.parameter_names, self.load.parameter_values):
                header += "  > " + str(i) + " : " + str(j) + "\n"

        return header

    def printHeader(self):
        """Prints program header with version"""
        print("pyfem1d - 1d finite elements for testing material formulations")
        #print(self.getHeader())

    def parseCmd(self):
        """Parses command line"""
        self.abspath = os.path.dirname(os.path.abspath(__file__))

        parser = argparse.ArgumentParser()
        parser.add_argument("input",
                            metavar="input_file",
                            nargs="?",
                            help="input file",
                            type=argparse.FileType("r"))
        # parser.add_argument("-o",
        #                     "--output-file",
        #                     default="default_out.dat",
        #                     type=argparse.FileType("w"))
        #parser.add_argument("-l", "--log-file", default="default.log",
        #type=argparse.FileType("w"))
        # parser.add_argument("-d",
        #                     "--displacement-file",
        #                     default="default_disp.dat",
        #                     type=argparse.FileType("w"))
        # parser.add_argument("-u",
        #                     "--stress-file",
        #                     default="default_stre.dat",
        #                     type=argparse.FileType("w"))
        # parser.add_argument("-p",
        #                     "--plot-file",
        #                     default="default.ps",
        #                     type=argparse.FileType("w"))
        # parser.add_argument("-n",
        #                     "--number-of-elements",
        #                     default="10",
        #                     type=int)

        # parser.add_argument("-t", "--timestep", default="0.1", type=float)
        # parser.add_argument("-m", "--maximum-time", default="25", type=float)
        # parser.add_argument("-g", "--gui", action="store_true", help="Start the graphical user interface")
        parser.add_argument("-v", "--verbose", action="store_true")
        # parser.add_argument("-s", "--silent", action="store_true")
        # parser.add_argument("-i", "--interactive", action="store_true")
        args = parser.parse_args()

        # self.silent = args.silent
        self.verbose = args.verbose
        # self.interactive = args.interactive
        # self.gui = args.gui

        # input file
        if args.input:
            self.inputFile = os.path.abspath(args.input.name)
            self.workingDirectory = os.path.dirname(os.path.abspath(
                args.input.name))
        else:
            self.workingDirectory = os.getcwd()

        #self.logFile = os.path.abspath(args.log_file.name)
        # self.outputFile = os.path.abspath(args.output_file.name)
        # self.stressFile = os.path.abspath(args.stress_file.name)
        # self.displacementFile = os.path.abspath(args.displacement_file.name)
        # self.plotFile = os.path.abspath(args.plot_file.name)

        self.outputFile = "default_out.dat"
        self.stressFile = "default_stre.dat"
        self.displacementFile = "default_disp.dat"

        self.add_umats(os.path.abspath(pyfem1d.umat_defaults.__file__))
        self.add_loads(os.path.abspath(pyfem1d.load_defaults.__file__))


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
    #"Starts the interactive IPython shell"
    #from IPython import embed
    #from IPython.config.loader import Config
    #cfg = Config()
    #cfg.TerminalInteractiveShell.confirm_exit = False
    #embed(config = cfg, user_ns = ns, display_banner = False)

    #def ipShell(self):
    #"Starts the interactive IPython shell
    #namespace defaults to __main__.__dict__"
    #from __main__ import __dict__ as ns
    #self.ipShellWithNamespace(ns)

    def plotToWindow(self, stressFile=None):
        if not stressFile:
            stressFile = self.stressFile
        commands = ""
        commands += "set terminal X11 size 1300 400;"
        commands += "set key rmargin;"
        commands += "set multiplot;"
        commands += "set lmargin at screen 0.025;"
        commands += "set rmargin at screen 0.325;"
        commands += "set xlabel \"Time\";"
        commands += "set ylabel \"Strain\";"
        commands += "plot \"%s\" u 1:2 w l;" % stressFile
        commands += "set lmargin at screen 0.35;"
        commands += "set rmargin at screen 0.65;"
        commands += "set ylabel \"Stress\";"
        commands += "plot \"%s\" u 1:3 w l;" % stressFile
        commands += "set lmargin at screen 0.675;"
        commands += "set rmargin at screen 0.975;"
        commands += "set xlabel \"Strain\";"
        commands += "plot \"%s\" u 2:3 w l;" % stressFile
        commands += "unset multiplot;"

        call(["gnuplot", "-p", "-e", commands])

#set output "| ps2pdf -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress - "+self.ofilebase+"_plot.pdf;\

    def plotPdf(self, stressFile, plotFile):
        # if not stressFile:
        #     stressFile = self.stressFile

        # if not plotFile:
        #     plotFile = self.plotFile

        print("Plotting to file %s" % plotFile)

        commands = ""
        commands += "set term pdf enhanced font \"Helvetica,10\";"
        commands += "set output \"%s\";" % plotFile
        commands += "set lmargin;"
        commands += "set rmargin;"
        commands += "set grid;"
        commands += "unset key;"
        commands += "set xlabel \"Time\";"
        commands += "set ylabel \"Strain\";"
        commands += "plot \"%s\" u 1:2 w l lt 1;" % stressFile
        commands += "set ylabel \"Stress\";"
        commands += "plot \"%s\" u 1:3 w l lt 1;" % stressFile
        commands += "set xlabel \"Strain\";"
        commands += "plot \"%s\" u 2:3 w l lt 1;" % stressFile

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

