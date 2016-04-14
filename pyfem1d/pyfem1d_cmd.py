import cmd
import sys
import os
# import pyfem1d.tkgui

class Pyfem1dShell(cmd.Cmd):
    intro = 'Type help or ? to list commands.\n'
    prompt = 'pyfem1d>> '
    file = None

    def __init__(self,parent):
        cmd.Cmd.__init__(self)
        #super(Pyfem1dShell, self).__init__()
        self.analysis = parent

    def do_verbose(self, arg):
        '''Enable verbose output'''
        self.analysis.execution.verbose = True
        #print(arg)

    # def do_gui(self, arg):
    #     '''Start graphical user interface'''
    #     pyfem1d.tkgui.startGui(self.analysis)

    def do_dt(self, arg):
        '''Set timestep size: dt value'''
        val, errormsg = parse_line(arg, type = float, n_args = 1)
        if not errormsg:
            self.analysis.execution.timestep = val[0]
        else:
            raise Exception(errormsg)

    def do_nelem(self, arg):
        '''Set total number of elements with nelem(value)'''
        val, errormsg = parse_line(arg, type = int, n_args = 1)
        if not errormsg:
            self.analysis.execution.number_of_elements = val[0]
        else:
            raise Exception(errormsg)

    def do_tmax(self, arg):
        '''Set maximum time tmax(value)'''
        val, errormsg = parse_line(arg, type = float, n_args = 1)
        if not errormsg:
            self.analysis.execution.maximum_time = val[0]
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

    def do_plotpdf(self, arg):
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

    def do_addumats(self, arg):
        '''Add umat material: addumat exampleMaterial.py'''
        val, errormsg = parse_line(arg, type = str, n_args = 1)
        if not errormsg:
            absModulePath = os.path.join(self.analysis.execution.workingDirectory, val[0])
            self.analysis.execution.add_umats(absModulePath)
        else:
            raise Exception(errormsg)

    def do_addloads(self, arg):
        '''Add loading function: addloading exampleLoading.py'''
        val, errormsg = parse_line(arg, type = str, n_args = 1)
        if not errormsg:
            absModulePath = os.path.join(self.analysis.execution.workingDirectory, val[0])
            self.analysis.execution.add_loads(absModulePath)
        else:
            raise Exception(errormsg)


    def do_load(self, arg):
        '''Set load function: load triangle '''
        val, errormsg = parse_line(arg, type = str, n_args = "1+")
        if not errormsg:
            self.analysis.execution.set_load(val[0])
            if len(val) > 1:
                parameters = tuple(map(float, val[1:]))
                self.analysis.execution.set_load_parameters(parameters)
        else:
            raise Exception(errormsg)

    def do_listumats(self, arg):
        '''List all umats with the parameters and their values'''
        self.list_umat_closure(self.analysis.execution.umat_dict)

    def do_listloads(self, arg):
        '''List all loading functions with the parameters and their values'''
        self.list_umat_closure(self.analysis.execution.load_dict)


    def list_umat_closure(self, dict_):
        for key, umat in dict_.items():
            print("  "+key+"(", end="")
            for n, (name, val) in enumerate(zip(umat.parameter_names, umat.parameter_values)):
                print(name+"="+str(val), end="")
                if n != len(umat.parameter_names)-1:
                    print(", ", end="")
            print(")")

    def do_umat(self, arg):
        '''Set umat function: umat maxwell '''
        val, errormsg = parse_line(arg, type = str, n_args = "1+")

        if not errormsg:
            self.analysis.execution.set_umat(val[0])
            if len(val) > 1:
                parameters = tuple(map(float, val[1:]))
                self.analysis.execution.set_umat_parameters(parameters)
        else:
            raise Exception(errormsg)


    def do_q(self, arg):
        '''End session'''
        self.close()
        return True

    def do_EOF(self,arg):
        '''End session'''
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
        # line = line.lower()
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
    if isinstance(n_args, str):
        if n_args[-1] == "+":
            min_limit = int(n_args[:-1])
            if len(result) < min_limit:
                errormsg = "expected minimum "+str(min_limit)+" arguments, received "+str(len(result))
            else:
                errormsg = None
    elif isinstance(n_args, int):
        if n_args and len(result) != n_args:
            errormsg = "expected "+str(n_args)+" arguments, received "+str(len(result))
        else:
            errormsg = None
    else:
        errormsg = None
    return result, errormsg

