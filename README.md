# feminist

1d finite elements for testing material formulations

## Installation

To install the python package, run `install` on `setup.py` which is located
in the project root directory

```
$ cd feminist/
$ python setup.py install
```

This will install the `feminist` module under `/usr/lib/python*/site-packages/feminist`, as well as the `feminist` script under `/usr/bin` which
is the primary handle for this program.

## Invocation

To run feminist, type in your command line:

```
$ feminist
feminist - 1d finite elements for testing material formulations
Type help or ? to list commands.

feminist>>
```

which drops you into the CLI for feminist. Here, you can type `help` to show a list of commands you can use.

In general, you can:

* run simulations directly inside the CLI,
* give input files to be executed,
* start the graphical user interface

To see all you options regarding the invocation of feminist, type in your command line:

```
$ feminist --help
usage: feminist [-h] [-o OUTPUT_FILE] [-d DISPLACEMENT_FILE] [-u STRESS_FILE]
                [-p PLOT_FILE] [-n NUMBER_OF_ELEMENTS] [-t TIMESTEP]
                [-m MAXIMUM_TIME] [--constitutive-dir CONSTITUTIVE_DIR]
                [--load-dir LOAD_DIR] [-g] [-v] [-s] [-i]
                [input_file]
...
```
### Some hints

* You can directly start the GUI with the `-g` flag.
* If you have given an input file and still want to use the CLI after the file is executed, you can give the `-i` option. You can also have the CLI and GUI at the same time with `-i -g` at the same time.

## Example feminist session: Using CLI commands

You can list the possible commands with the command `help`.
```
feminist>> help
Documented commands (type help <topic>):
========================================
bctype  help   plotps           setconstitutivepars  solve  
dt      nelem  quit             setloading           tmax
gui     plot   setconstitutive  setloadingpars       verbose
...
```

Here is an example session which fully utilizes most of the commands you need to run a simulation:
```
feminist - 1d finite elements for testing material formulations
Type help or ? to list commands.

feminist>> bctype 2
feminist>> tmax 25
feminist>> nelem 10
feminist>> setloading triangle
feminist>> setloadingpars 10 0.005
feminist>> setconstitutive maxwell
feminist>> setconstitutivepars 200 3000
feminist>> solve
 Input file   : None
 Output file  : /home/onur/default_out.dat
 Stress file  : /home/onur/default_stre.dat
 Disp. file   : /home/onur/default_disp.dat
 The following parameters have been set:
 Number of Elements    nelem = 10
 Time step size           dt = 0.1000
 Duration               tmax = 25.0000
 Boundary Condition   bctype = 0
 Material model : maxwell
  > elastic_mod : 200.0
  > viscosity : 3000.0
 Loading function: triangle
  > loading_per : 10.0
  > magnitude : 0.005

=== END OF PROCESSING ===
feminist>> plot
feminist>> plotps
Plotting to file /home/onur/default.ps
```

1. Boundary condition type is set to displacement driven clamped 1d bar (bctype = 2).
2. Maximum time for the simulation is set to 25 time units.
3. Number of elements is set to 10.
4. The loading function is selected as `triangle`.
5. Parameters for the triangle function are selected as parameter_1 = 10 and parameter_2 = 0.005. Note that you can define any loading function with any parameters for your own purposes. This is also valid for the constitutive functions for materials.
6. The constitutive function is selected as `maxwell`.
7. The parameters to the constitutive function are given the same way as the loading function. Again, note that you can define any parameter inside the specific files for materials, see the next section regarding adding new materials.
8. The simulation is started by the `solve` command.
9. After the simulation ends, the user can type `plot` to see the results with `gnuplot`.
10. The results can also be plotted to a postscript file with the `plotps` command.


## Example input File

An input for feminist is composed of input lines you would normally enter in feminist's CLI. You can collect these commands in a file and run them directly for faster results.
```
# ex1.txt:
bctype 2

setloading triangle
setloadingpars 10 0.005

setconstitutive maxwell
setconstitutivepars 200 3000

solve
plot
plotps ex1.pdf
```

You can then execute the commands by invoking feminist with the filename without any flags,
```
$ feminist ex1.txt
```
This will run through the lines and execute each line, and even plot the results into the postscript file `ex1.ps`. You can use this to your advantage in many ways; for example exploring the parameter space by batch assigning different material parameters and observing the response.

## Adding a new constitutive function (AKA adding a new material)
