from __future__ import division, print_function, absolute_import
import cmd
import sys
import os
import feminist.tkgui

class FeministShell(cmd.Cmd):
    intro = 'Type help or ? to list commands.\n'
    prompt = 'feminist>> '
    file = None

    def __init__(self,parent):
        cmd.Cmd.__init__(self)
        #super(FeministShell, self).__init__()
        self.analysis = parent

    def do_verbose(self, arg):
        '''Enable verbose output'''
        self.analysis.execution.verbose = True
        #import pdb; pdb.set_trace()
        #print(arg)

    def do_gui(self, arg):
        '''Start graphical user interface'''
        feminist.tkgui.startGui(self.analysis)

    def do_dt(self, arg):
        '''Set timestep size: dt value'''
        val, errormsg = parse_line(arg, type = float, n_args = 1)
        if not errormsg:
            self.analysis.execution.dt = val[0]
        else:
            raise Exception(errormsg)

    def do_nelem(self, arg):
        '''Set total number of elements with nelem(value)'''
        val, errormsg = parse_line(arg, type = int, n_args = 1)
        if not errormsg:
            self.analysis.execution.nelem = val[0]
        else:
            raise Exception(errormsg)

    def do_tmax(self, arg):
        '''Set maximum time tmax(value)'''
        val, errormsg = parse_line(arg, type = float, n_args = 1)
        if not errormsg:
            self.analysis.execution.tmax = val[0]
        else:
            raise Exception(errormsg)

    def do_bctype(self, arg):
        '''Set bc type with bctype(val), can be 0,1,2'''
        val, errormsg = parse_line(arg, type = int, n_args = 1)
        if not errormsg:
            if val[0] == 0 or val[0] == 1 or val[0] == 2:
                self.analysis.execution.bctype = val[0]
            else:
                raise Exception("Error: bctype can only be one of 0, 1 and 2")
        else:
            raise Exception(errormsg)


    def do_solve(self, arg):
        '''Start solution with solve()'''
        self.analysis.solve()

    def do_plot(self, arg):
        '''Plot the output stress file using gnuplot. optional argument: stressFile'''
        val, errormsg = parse_line(arg, type = str)
        if len(val) == 0:
            stressFile = self.analysis.execution.stressFile
        elif len(val) == 1:
            stressFile = val[0]
        else:
            raise Exception("Error: plot cannot receive more than 1 arguments")

        self.analysis.execution.plotToWindow(stressFile=stressFile)

    def do_plotps(self, arg):
        '''Plot the output stress file to a pdf file using gnuplot. optional arguments: plotFile stressFile'''
        val, errormsg = parse_line(arg, type = str)
        if len(val) == 0:
            plotFile = self.analysis.execution.plotFile
            stressFile = self.analysis.execution.stressFile
        elif len(val) == 1:
            plotFile = val[0]
            stressFile = self.analysis.execution.stressFile
        elif len(val) == 2:
            plotFile = val[0]
            stressFile = val[1]
        else:
            raise Exception("Error: plot cannot receive more than 2 arguments")

        self.analysis.execution.plotPdf(stressFile=stressFile, plotFile=plotFile)

    def do_pwd(self, arg):
        'Prints current working directory'
        print(self.analysis.execution.workingDirectory)

    #def do_cd(self, arg):
        #'Changes current working directory'

    def do_addconstitutive(self, arg):
        '''Add constitutive material: addconstitutive exampleMaterial.py'''
        val, errormsg = parse_line(arg, type = str, n_args = 1)
        if not errormsg:
            absModulePath = os.path.join(self.analysis.execution.workingDirectory, val[0])
            self.analysis.execution.constitutive.addModule(absModulePath)
        else:
            raise Exception(errormsg)

    def do_addloading(self, arg):
        '''Add loading function: addloading exampleLoading.py'''
        val, errormsg = parse_line(arg, type = str, n_args = 1)
        if not errormsg:
            absModulePath = os.path.join(self.analysis.execution.workingDirectory, val[0])
            self.analysis.execution.load.addModule(absModulePath)
        else:
            raise Exception(errormsg)

    def do_setloading(self, arg):
        '''Set loading function: setLoading triangle'''
        val, errormsg = parse_line(arg, type = str, n_args = 1)
        if not errormsg:
            self.analysis.execution.load.setFunction(val[0])
        else:
            raise Exception(errormsg)

    def do_setconstitutive(self, arg):
        '''Set constitutive function: setLoading maxwell '''
        val, errormsg = parse_line(arg, type = str, n_args = 1)
        if not errormsg:
            self.analysis.execution.constitutive.setFunction(val[0])
        else:
            raise Exception(errormsg)

    def do_setconstitutivepars(self, arg):
        '''Set constitutive function parameters: setConstitutiveParameterValues 100 200 300'''
        val, errormsg = parse_line(arg, type = float)
        self.analysis.execution.constitutive.setParameterValues(val)

    def do_setloadingpars(self, arg):
        '''Set loading function parameters: setLoadingParameterValues 100 200 300'''
        val, errormsg = parse_line(arg, type = float)
        self.analysis.execution.load.setParameterValues(val)

    def do_quit(self, arg):
        'End session'
        self.close()
        return True

    def do_eof(self,arg):
        self.close()
        return True

    # ----- record and playback -----
    #def do_record(self, arg):
        #'Save future commands to filename:  RECORD rose.cmd'
        #self.file = open(arg, 'w')
    #def do_playback(self, arg):
        #'Playback commands from a file:  PLAYBACK rose.cmd'
        #self.close()
        #with open(arg) as f:
            #self.cmdqueue.extend(f.read().splitlines())

    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

    def execFile(self, filename):
        f = open( filename, "r" )
        array = []
        for line in f:
            array.append( line )
        f.close()
        for i,j in enumerate(array):
            try:
                line = cleanLine(j)
                if(line):
                    #print("Executing: "+line)
                    self.onecmd(line)
            except Exception as err:
                raise Exception("line "+str(i)+": "+j+str(err))


def cleanLine(line):
    return line.split('#')[0].strip()

def parse_line(arg, n_args = None, type=int):
    'Convert a series of zero or more numbers to an argument tuple'
    result = tuple(map(type, arg.split()))
    if n_args and len(result) != n_args:
        errormsg = "expected "+str(n_args)+" arguments, received "+str(len(result))
    else:
        errormsg = None
    return result, errormsg

