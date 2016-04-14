import sys, os
import pyfem1d.execution as execution_
import pyfem1d.pyfem1d_cmd as cmd_
import numpy as np
import collections


class Analysis:
    '''Class to hold everythin relevant to the 1D FE analysis'''

    def __init__(self):
        self.execution = execution_.Execution()
        self.cmdShell = cmd_.Pyfem1dShell(self)

    def startShell(self):
        self.cmdShell.cmdloop()

    def setRuntimeParameters(self):
        self.o_node = self.execution.number_of_elements + 1  #node to be written to the output
        self.o_elem = self.execution.number_of_elements  #element to be written to the output
        self.number_of_elements = self.execution.number_of_elements
        self.neq = self.execution.number_of_elements + 1
        self.nnode = self.execution.number_of_elements + 1
        self.t = 0

        if isinstance(self.execution.bctype, collections.Iterable):
            self.execution.bctype = 0

    def solve(self):
        '''Solution function'''

        if not self.execution.umat:
            raise Exception("No umat function specified")

        if not self.execution.load:
            raise Exception("No load function specified")

        if not self.execution.maximum_time:
            raise Exception("No end time specified")

        if not self.execution.number_of_elements:
            raise Exception("No number of elements specified")

        if not self.execution.timestep:
            raise Exception("No timestep specified")

        self.setRuntimeParameters()
        output = open(self.execution.outputFile, 'w')

        #self.update()

        print(self.execution.getHeader())
        output.write(self.execution.getHeader())
        #self.printheader(ofile=output)

        neq = self.execution.number_of_elements + 1
        #Initialize the system matrices
        self.init_system()
        #Set time to zero
        self.t = 0.
        #Generate nodes &  initialize solution vector
        dl = 1 / self.execution.number_of_elements
        u = execution_.zeros((self.neq, 1))
        x = execution_.zeros((self.nnode, 1))
        #u= zeroflt(self.neq,1)
        #x= zeroflt(self.nnode,1)
        for i in range(int(self.nnode)):
            x[i] = (i - 1) * dl

        # open files for output at the selected node and element
        outd = open(self.execution.displacementFile, 'w')
        outs = open(self.execution.stressFile, 'w')

        # Simulation loop

        self.execution.umat.initial_cond(self.execution.number_of_elements)
        # if self.execution.umat.initcond():
        #     self.execution.umat.initcond()(self.execution.number_of_elements)

        while self.t <= self.execution.maximum_time + self.execution.timestep:

            load = self.execution.load.value(self.t)
            if self.execution.verbose:
                print('   Compute solution at t= %6.4f, load= %6.4f' %
                      (self.t, load))

            # Newton iterations
            res = 1
            niter = 0
            nitermax = 50
            while res > 1.e-10 and niter < nitermax:
                #Calculate the residual vector and stiffness matrix
                #and update the history variables
                self.comp_stiffness(u)
                #impose boundary conditions
                if self.execution.bctype == 0:
                    self.kg[:][0] = 0.
                    self.kg[0][:] = 0.
                    self.kg[0][0] = 1.
                    self.fg[-1] -= load
                    self.fg[0] = 0.
                elif self.execution.bctype == 2:
                    du = load - u[-1]
                    for i in range(int(neq)):
                        self.fg[i] -= self.kg[i][-1] * du
                    self.kg[:][0] = 0.
                    self.kg[0][:] = 0.
                    self.kg[-1][:] = 0
                    self.kg[:][-1] = 0
                    self.kg[0][0] = 1.
                    self.kg[-1][neq - 1] = 1.
                    self.fg[0] = 0.
                    self.fg[-1] = -1 * du
                elif self.execution.bctype == 1:
                    self.kg[:][0] = 0.
                    self.kg[0][:] = 0.
                    self.kg[0][0] = 1.
                    self.fg[1:-1] -= load * dl
                    self.fg[-1] = self.fg[-1] - load * dl / 2
                    self.fg[0] = 0
                else:
                    raise Exception('Error: Undefined bc type identifier: ' +
                                    self.execution.bctype)
                #calculate the residual
                res = np.linalg.norm(self.fg, 2)
                if self.execution.verbose:
                    print('  >> iter %2i, res = %10.5e' % (niter, res))
                #solve the system
                kginv = np.linalg.inv(self.kg)
                dg = np.dot(kginv, self.fg)
                #update nodal displacements
                u -= dg
                niter += 1
            # Print results
            #if self.execution.verbose:
            output.write('\n Solution at t=%6.4f, load= %6.4f\n' %
                         (self.t, load))
            output.write('  Nodal solutions\n')
            output.write('  Node   x-coord.     u\n')
            for i in range(int(neq)):
                output.write(' %4i    %6.4e   %6.4e\n' % (i, x[i], u[i]))
            output.write('\n  Element solutions\n')
            output.write('  Element   Strain       Stress\n')
            for i in range(int(self.number_of_elements)):
                output.write(' %4i       %6.4e   %6.4e\n' %
                             (i, self.eps[i], self.sig[i]))
            outd.write(' %6.4e   %6.4e\n' % (self.t, u[self.o_node - 1]))
            outs.write(' %6.4e   %6.4e   %6.4e\n' % (
                self.t, self.eps[self.o_elem - 1], self.sig[self.o_elem - 1]))

            # Update History
            if self.execution.umat.update():
                self.execution.umat.update()()

            self.t += self.execution.timestep

        print('Finished solution')
        outd.close()
        outs.close()
        output.close()

    def init_system(self):
        self.fg = execution_.zeros((self.neq, 1))
        self.kg = execution_.zeros((self.neq, self.neq))
        self.eps = execution_.zeros((self.number_of_elements, 1))
        self.sig = execution_.zeros((self.number_of_elements, 1))
        self.aa = execution_.zeros((self.number_of_elements, 1))
        #self.fg=zeroflt(self.neq,1)
        #self.kg=zeroflt(self.neq,self.neq)
        #self.eps=zeroflt(self.number_of_elements,1)
        #self.sig=zeroflt(self.number_of_elements,1)
        #self.aa=zeroflt(self.number_of_elements,1)
        self.dl = 1 / float(self.number_of_elements)

    def comp_stiffness(self, u):
        '''Compute stiffness matrix and residual vector,
        and update history variables'''
        offs = 0
        self.fg[:] = 0.
        self.kg[:][:] = 0.
        dN = execution_.zeros((2, 1))
        #dN=zeroflt(2,1)
        # Assembly: loop over elements
        for n in range(int(self.number_of_elements)):
            dN[0] = -1 / self.dl
            dN[1] = -1 * dN[0]
            #compute element strain
            epsl = (u[n + 1] - u[n]) / self.dl
            # Calculate the stress, modulus and update history at the Gauss point

            sigl, aal = self.execution.umat.stress_tangent(self.execution.timestep,
                                                   n, epsl)

            #store the stresses and moduli
            self.eps[n] = epsl
            self.sig[n] = sigl
            self.aa[n] = aal
            #loop over element dofs: element stiffness and internal force vector
            #fe = zeroflt(2,1)
            #ke = zeroflt(2,2)
            fe = execution_.zeros((2, 1))
            ke = execution_.zeros((2, 2))
            for i in range(2):
                fe[i] += dN[i] * sigl * self.dl
                #\int B^{T}\sigma dV
                for j in range(2):
                    ke[i][j] += dN[i] * aal * dN[
                        j] * self.dl  #\int B^{T} E B dV

            #assemble global matrices
            for i in range(2):
                self.fg[i + offs] += fe[i]
                for j in range(2):
                    self.kg[i + offs][j + offs] += ke[i][j]
            offs += 1
