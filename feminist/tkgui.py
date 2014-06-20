from __future__ import division, print_function, absolute_import

from Tkinter import *
from multiprocessing import Process
import os

boxWidth = 15

class OptionBox(OptionMenu):
    def __init__(self,parent,function,r,c):
        self.value = StringVar()
        self.value.set(function.listt[function.defaultind])
        self.box = OptionMenu(parent, self.value, *function.listt)
        self.box.grid(row = r, column = c, sticky = N+S+E+W)
        self.box.config(width = boxWidth, anchor = W)
    def get(self):
        return self.value.get()


class OptionBox2(OptionMenu):
    def __init__(self,parent,outerind,listt,vallist,r,c,ind = 0):
        self.value = StringVar()
        self.value.set(listt[ind])
        self.box = OptionMenu(parent, self.value, *listt)
        self.listt = listt
        self.vallist = vallist
        self.ind = ind
        self.outerind = outerind
        self.box.grid(row = r, column = c, sticky = N+S+E+W)
        self.box.config(width = boxWidth, anchor = W)

    def get(self):
        return self.value.get()

    def getIndex(self):
        for i,j in zip(range(len(self.listt)),self.listt):
            if self.get() == j:
                return i

    def getcurrval(self):
        return self.vallist[self.getIndex()]


class ParameterFrame(Frame):
    def __init__(self,parent,function):
        if type(function) != type('a'):
            raise Exception('Error: pass the module name as a string')
        self.parent = parent

        # go up one level if the parent's parent exists
        if hasattr(self.parent, 'parent'):
            self.parent = self.parent.parent

        self.function = function  #string

        Frame.__init__(self, parent)
        self.createwidgets()

    def createwidgets(self):
        self.labels = []; self.entries = []; self.optionBoxList = []
        list2 = self.parent.an.execution.__dict__[self.function].getMetavars()
        size = self.parent.an.execution.__dict__[self.function].size
        for n in range(size):
            optionBoxBool = False
            if hasattr(self.parent.an.execution.__dict__[self.function], 'parameters'):
                if self.parent.an.execution.__dict__[self.function].parameters[n].options:
                    optionBoxBool = True
            if optionBoxBool:
                variable = self.parent.an.execution.__dict__[self.function].parameters[n].variable
                self.optionBoxList.\
                    append(OptionBox2(self,n,\
                                      self.parent.an.execution.__dict__[self.function].parameters[n].options,\
                                      self.parent.an.execution.__dict__[self.function].__dict__[variable]\
                                      ,n,1))
            else:
                self.entries.append(makeEntry(self,n,1))

            self.labels.append(makeLabel(self,n,0,list2[n]))

        self.grid(columnspan = 2,rowspan = size)

    def give(self):
        entry = []
        newParameters = []
        entind = 0
        size = self.parent.an.execution.__dict__[self.function].size
        for i in range(size):
            dummy = 0
            for j in self.optionBoxList:
                if j.outerind == i:
                  newParameters.append(j.getcurrval())
                  dummy = 1
                  break
            if dummy == 1:
                continue
            newParameters.append(float(self.entries[entind].get()))
            entind += 1
        # for i in self.optionBoxList:
        #     vars(varss(self.function))[i.name] = i.getcurrval()

        # for i in self.entries:
        #     entry.append(float(i.get()))
        self.parent.an.execution.__dict__[self.function].setParameterValues(newParameters)

    def take(self):
        for i,j in zip(self.parent.an.execution.__dict__[self.function].getParameterValues(),self.entries):
            j.insert(0,str(i))


class FunctionFrame(Frame):
    def __init__(self,parent,function):
        self.parent = parent
        Frame.__init__(self, parent)
        self.function = function
        self.createwidgets()
        self.box.value.trace('w',self.loadFunction)
        self.loadFunction()

    def createwidgets(self):
        self.box = OptionBox(self,self.parent.an.execution.__dict__[self.function],0,1)
        self.label = makeLabel(self,0,0,self.parent.an.execution.__dict__[self.function].modname)

    def loadFunction(self,*args):
        size = self.parent.an.execution.__dict__[self.function].size
        self.parent.an.execution.__dict__[self.function].setFunction(self.box.get())
        if hasattr(self,'parameterFrame'):
            self.parameterFrame.destroy()
        self.parameterFrame = ParameterFrame(self,self.function)
        self.grid(rowspan = size+1)
        self.parameterFrame.grid(row = 1,column = 0)
        self.take()

    def give(self):
        self.parameterFrame.give()

    def take(self):
        self.parameterFrame.take()


class Application(Frame):
    def __init__(self, analysis, master = None):
        self.an = analysis
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.takeParameters()
        self.processes = []

    def createWidgets(self):
        self.mainparFrame = ParameterFrame(self,'mainpar')
        self.mainparFrame.grid(row = 0,column = 0)

        self.labels = []
        self.ldict = {'r':[],'c':[],'text':[]}
        self.ldict['r'][:] = [3]
        self.ldict['c'][:] = [0]
        self.ldict['text'][:] = ['BC type']

        # Simulation button
        self.solveButton = Button(self, text = "Run", command = self.startSolution)
        self.solveButton.grid(row = 10,column = 0,columnspan = 2,sticky = N+S+W+E)
        #self.solveButton.config(width = 17)

        # Termination button
        self.haltButton = Button(self, text = "Halt", command = self.halt)
        self.haltButton.grid(row = 11,column = 0,columnspan = 2,sticky = N+S+W+E)
        #self.haltButton.config(width = 17)

        # Plotting
        self.plotButton = Button(self, text = "Plot", command = self.an.execution.plotPdf)
        self.plotButton.grid(row = 12,column = 0,columnspan = 2,sticky = N+S+W+E)
        #self.plotButton.config(width = 17)
        #self.met = progress.Meter(self,relief = 'ridge', bd = 3,width = 250)
        #self.met.grid(row = 10,column = 0)

        self.constFrame = FunctionFrame(self,'constitutive')
        self.constFrame.grid(row = 0,column = 3)
        self.loadFrame = FunctionFrame(self,'load')
        self.loadFrame.grid(row = 0,column = 4)

    def takeParameters(self):
        self.mainparFrame.take()
        #self.constFrame.take()
        #self.loadFrame.take()

    def giveParameters(self):
        self.mainparFrame.give()
        self.constFrame.give()
        self.loadFrame.give()

    def startSolution(self):
        self.giveParameters()
        self.processes.append(Process(target = self.solve))
        self.processes[-1].start()

    def solve(self):
        #import cProfile
        #cProfile.run('self.an.solve()')
        self.an.solve()
        self.an.execution.plotToWindow()

    def halt(self):
        for i in self.processes:
            i.terminate()
        print('== Solution halted ==')


def guiStarterHandle(an):
    root = Tk()
    app = Application(an, master = root)
    app.mainloop()
    #root.destroy()

def startGui(an):
    guiProcess = Process(target = guiStarterHandle, args=(an,))
    guiProcess.start()

def makeEntry(parent,r,c):
    entry = Entry(parent)
    entry.grid(row = r,column = c,sticky = N+S+E+W)
    entry.config(width = boxWidth)
    return entry

def makeLabel(parent,r,c,textz):
    label = Label(parent,text = textz,anchor = W)
    label.grid(row = r,column = c,sticky = N+S+E+W)
    label.config(width = boxWidth,height = 1)
    return label


