# pyfem1d

1d finite elements for testing material formulations

### Dependencies

* Python 3.0 or higher
* NumPy
* gnuplot

## Installation

To install the python package, run `install` on `setup.py` which is located
in the project root directory

```
$ cd pyfem1d/
$ python setup.py install
```

This will install the `pyfem1d` module under
`/usr/lib/python*/site-packages/pyfem1d`, as well as the `pyfem1d` script under
`/usr/bin` which is the primary handle for this program.

## Usage

To run pyfem1d, type in your command line:

```
$ pyfem1d
pyfem1d - 1d finite elements for testing material formulations
Type help or ? to list commands.

pyfem1d>>
```

which drops you into the CLI for pyfem1d. Here, you can type `help` to show a
list of commands you can use.

In general, you can:

* run simulations directly inside the CLI,
* give input files to be executed,
* start the graphical user interface

To see all you options regarding the invocation of pyfem1d, type in your command
line:

```
$ pyfem1d --help
usage: main.py [-h] [-v] [input_file]

positional arguments:
  input_file     input file

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
```
### Some hints

* You can directly start the GUI with the `-g` flag.
* If you have given an input file and still want to use the CLI after the file
  is executed, you can give the `-i` option. You can also have the CLI and GUI
  at the same time with `-i -g` at the same time.

## Example pyfem1d session: Using CLI commands

You can list the possible commands with the command `help`.
```
Documented commands (type help <topic>):
========================================
EOF       addumats  dt    listloads  load   plot     pwd  solve  umat
addloads  bctype    help  listumats  nelem  plotpdf  q    tmax   verbose
```

Here is an example session which fully utilizes most of the commands you need to
run a simulation:

```
pyfem1d - 1d finite elements for testing material formulations
Type help or ? to list commands.

pyfem1d>> bctype 2
pyfem1d>> tmax 25
pyfem1d>> nelem 10
pyfem1d>> dt 0.1
pyfem1d>> load Triangle 10 0.005
pyfem1d>> umat Maxwell 200 3000
pyfem1d>> solve
 Input file   : None
 Output file  : default_out.dat
 Stress file  : default_stre.dat
 Disp. file   : default_disp.dat
 The following parameters have been set:
 Number of Elements    nelem = 10
 Time step size           dt = 0.1000
 Duration               tmax = 25.0000
 Boundary Condition   bctype = 2
 Material model : Maxwell
  > elastic_mod : 200.0
  > viscosity : 3000.0
 Loading function: Triangle
  > loading_per : 10.0
  > magnitude : 0.005

Finished solution
pyfem1d>> plot
pyfem1d>> plotpdf output.pdf
Plotting to file output.pdf
```

1. Boundary condition type is set to displacement driven clamped 1d bar (bctype = 2).
2. Maximum time for the simulation is set to 25 time units.
3. Number of elements is set to 10.
3. Time-step is set to 0.1.
4. The loading function is selected as `Triangle`.
5. Parameters for the triangle function are selected as parameter\_1 = 10 and
   parameter\_2 = 0.005. Note that you can define any loading function with any
   parameters for your own purposes. This is also valid for the umat functions
   for materials.
6. The umat function is selected as `Maxwell`.
7. The parameters to the umat function are given the same way as the loading
   function. Again, note that you can define any parameter inside the specific
   files for materials, see the next section regarding adding new materials.
8. The simulation is started by the `solve` command.
9. After the simulation ends, the user can type `plot` to see the results with `gnuplot`.
10. The results can also be plotted to a postscript file with the `plotpdf` command.


## Example input File

An input for pyfem1d is composed of input lines you would normally enter in
pyfem1d's CLI. You can collect these commands in a file and run them directly
for faster results.
```
# ex1.txt:

bctype 2
tmax 25
nelem 10
dt 0.1

load Triangle 10 0.005

umat Maxwell 200 300

solve

plot

plotpdf output.pdf
```

You can then execute the commands by invoking pyfem1d with the filename without
any flags,
```
$ pyfem1d ex1.txt
```
This will run through the lines and execute each line, and even plot the results
into the postscript file `output.pdf`. You can use this to your advantage in many
ways; for example exploring the parameter space by batch assigning different
material parameters and observing the response.

<!-- ## Adding a new umat (AKA adding a new material) -->
