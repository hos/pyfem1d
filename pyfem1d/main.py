import pyfem1d.analysis
from multiprocessing import Process

def __main__():
    an = pyfem1d.analysis.Analysis()
    an.execution.parseCmd()

    an.execution.printHeader()

    # Execute the input file if given
    if an.execution.inputFile:
        an.cmdShell.execFile(an.execution.inputFile)
        #execfile(an.execution.inputFile)

    # Start gui if -g was used
    # if an.execution.gui:
    #     pyfem1d.tkgui.startGui(an)

    # Start interactive shell if -i was given or
    # there was neither input file nor -g
    # if an.execution.interactive or (not an.execution.inputFile and not an.execution.gui):
    if not an.execution.inputFile:
        an.startShell()


if __name__ == "__main__":
    __main__()
