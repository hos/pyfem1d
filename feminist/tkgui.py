from __future__ import division, print_function, absolute_import

from Tkinter import *
from multiprocessing import Process
import os
#import progress

boxwidth = 15

class optbox(OptionMenu):
    def __init__(self,parent,fun,r,c):
        self.val=StringVar()
        self.val.set(fun.listt[fun.defaultind])
        self.box = OptionMenu(parent, self.val, *fun.listt)
        self.box.grid(row=r,column=c,sticky=N+S+E+W)
        self.box.config(width=boxwidth,anchor=W)
    def get(self):
        return self.val.get()

class optbox2(OptionMenu):
    def __init__(self,parent,outerind,listt,vallist,r,c,ind=0):
        self.val=StringVar()
        self.val.set(listt[ind])
        self.box = OptionMenu(parent, self.val, *listt)
        self.listt=listt
        self.vallist=vallist
        self.ind=ind
        self.outerind=outerind
        self.box.grid(row=r,column=c,sticky=N+S+E+W)
        self.box.config(width=boxwidth,anchor=W)
    def get(self):
        return self.val.get()
    def getind(self):
        for i,j in zip(range(len(self.listt)),self.listt):
            if self.get()==j:
                return i
    def getcurrval(self):
        return self.vallist[self.getind()]


class parframe(Frame):
    def __init__(self,parent,fun):
        if type(fun)!=type('a'):
            raise Exception('Error: pass the module name as a string')
        self.parent = parent
        try:
            self.parent = self.parent.parent
        except:
            pass
        self.fun=fun  #string

        Frame.__init__(self, parent)
        self.createwidgets()

    def createwidgets(self):
        self.labels=[]; self.entries=[]; self.optboxi=[]
        list2 = self.parent.an.execution.__dict__[self.fun].getMetavars()
        size = self.parent.an.execution.__dict__[self.fun].size
        for n in range(size):
            optboxBool = False
            if hasattr(self.parent.an.execution.__dict__[self.fun], 'parameters'):
                if self.parent.an.execution.__dict__[self.fun].parameters[n].options:
                    optboxBool = True
            if optboxBool:
                variable = self.parent.an.execution.__dict__[self.fun].parameters[n].variable
                self.optboxi.append(optbox2(self,n,\
                                            self.parent.an.execution.__dict__[self.fun].parameters[n].options,\
                                            self.parent.an.execution.__dict__[self.fun].__dict__[variable]\
                                            ,n,1))
            else:
                self.entries.append(makent(self,n,1))

            self.labels.append(makel(self,n,0,list2[n]))

        self.grid(columnspan=2,rowspan=size)

    def give(self):
        ent=[]
        newpars=[]
        entind=0
        size = self.parent.an.execution.__dict__[self.fun].size
        for i in range(size):
            dummy=0
            for j in self.optboxi:
                if j.outerind==i:
                  newpars.append(j.getcurrval())
                  dummy=1
                  break
            if dummy==1:
                continue
            newpars.append(float(self.entries[entind].get()))
            entind+=1
        # for i in self.optboxi:
        #     vars(varss(self.fun))[i.name]=i.getcurrval()

        # for i in self.entries:
        #     ent.append(float(i.get()))
        self.parent.an.execution.__dict__[self.fun].setParameterValues(newpars)
    def take(self):
        for i,j in zip(self.parent.an.execution.__dict__[self.fun].getParameterValues(),self.entries):
            j.insert(0,str(i))


class funframe(Frame):
    def __init__(self,parent,fun):
        self.parent = parent
        Frame.__init__(self, parent)
        self.fun=fun
        self.createwidgets()
        self.box.val.trace('w',self.loadfun)
        self.loadfun()
    def createwidgets(self):
        self.box=optbox(self,self.parent.an.execution.__dict__[self.fun],0,1)
        self.lbl=makel(self,0,0,self.parent.an.execution.__dict__[self.fun].modname)

    def loadfun(self,*args):
        size = self.parent.an.execution.__dict__[self.fun].size
        self.parent.an.execution.__dict__[self.fun].setFunction(self.box.get())
        if hasattr(self,'parfr'):
            self.parfr.destroy()
        self.parfr=parframe(self,self.fun)
        self.grid(rowspan=size+1)
        self.parfr.grid(row=1,column=0)
        self.take()
    def give(self):
        self.parfr.give()
    def take(self):
        self.parfr.take()


class Application(Frame):

    def createWidgets(self):
        self.mainparframe=parframe(self,'mainpar')
        self.mainparframe.grid(row=0,column=0)

        self.labels=[]
        self.ldict={'r':[],'c':[],'text':[]}
        self.ldict['r'][:]=[3]
        self.ldict['c'][:]=[0]
        self.ldict['text'][:]=['BC type']

        #SIMULATION BUTTON
        self.simbut = Button(self, text="RUN", command=self.runsim)
        self.simbut.grid(row=10,column=0,columnspan=2,sticky=N+S+W+E)
        #self.simbut.config(width=17)
        #TERMINATION BUTTON
        self.haltbut = Button(self, text="HALT", command=self.halt)
        self.haltbut.grid(row=11,column=0,columnspan=2,sticky=N+S+W+E)
        #self.haltbut.config(width=17)
        #PLOTTING
        self.plotbut = Button(self, text="PLOT", command=self.an.plotPdf)
        self.plotbut.grid(row=12,column=0,columnspan=2,sticky=N+S+W+E)
        #self.plotbut.config(width=17)
        #self.met=progress.Meter(self,relief='ridge', bd=3,width=250)
        #self.met.grid(row=10,column=0)

        self.consframe=funframe(self,'constitutive')
        self.consframe.grid(row=0,column=3)
        self.loadframe=funframe(self,'load')
        self.loadframe.grid(row=0,column=4)

    def takepars(self):
        self.mainparframe.take()
        #self.consframe.take()
        #self.loadframe.take()

    def givepars(self):
        #import cfg as cf
        #parfrgive(self.consframe.parfr,cf.constitutive)
        #parfrgive(self.loadframe.parfr,cf.loading)
        #parfrgive(self.mainparframe,cf)
        self.mainparframe.give()
        self.consframe.give()
        self.loadframe.give()


        #bctext=self.bcbox.get()
        #cf.bctype=int(bctext[0])
        #updatevars()

    def runsim(self):
        #progval(self.met,cf.t/cf.tmax)

        self.givepars()
        #global p,p2
        self.p.append(Process(target=self.sim))
        self.p[-1].start()
        #p2 = Process(target=self.progval,args=(self.met,cf.t/cf.tmax))
        #p2.start()
        #self.progval(self.met,0)
    def sim(self):
        #import cProfile
        #cProfile.run('self.an.solve()')
        self.an.solve()
        self.an.plotToWindow()


    def halt(self):
        for i in self.p:
            i.terminate()
        #p2.terminate()
        print('================HALT===============')



    def __init__(self, analysis, master=None):
        #cf.constest() #Test for the constitutive equations
        #self.an = analysis.Analysis()
        self.an = analysis
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.takepars()
        self.p=[]

def startGui(an):
    root = Tk()
    app = Application(an, master=root)
    app.mainloop()
    #root.destroy()

def makent(parent,r,c):
    ent=Entry(parent)
    ent.grid(row=r,column=c,sticky=N+S+E+W)
    ent.config(width=boxwidth)
    return ent

def makel(parent,r,c,textz):
    lbl=Label(parent,text=textz,anchor=W)
    lbl.grid(row=r,column=c,sticky=N+S+E+W)
    lbl.config(width=boxwidth,height=1)
    return lbl

def insval(ent,var):
    ent.insert(0,str(var))


    # def progval(self,meter,val):

    #     while val<=0.99:
    #         print cf.t
    #         meter.set(val)
    #         val=float(cf.t/cf.tmax)
    #         sleep(0.05)
    #         print val
    #     print val
    #     self.terminate()




