# User's Guide

Salsa Dancing Molecules aims to provide code for running MD
simulations on super computers, visualising the results, and
publishing the results.

# Developing

To perform development, enable your Conda environment or virtual
environment, then use pip to configure the module to be installed in
editable mode.

## Conda

In the project top directory, do

    conda create -n salsa_dancing_molecules
    source activate salsa_dancing_molecules
    conda install pip
    pip install numpy # needed because of broken asap3 dependencies
    pip install -e .
    conda install -c conda-forge openkim_models kim-api kimpy

and answer yes to all questions to create an environment called
salsa_dancing_molecules, activate it and install Salsa Dancing
Molecules in development mode into it. If successful, the program can
be run with

    salsa-dancing-molecules

which will run the current source code straight from the project.

The installation step only needs to be done once and during future
development sessions, it is enough to issue

    source activate salsa_dancing_molecules

to enter the development environment.

## Virtual environment

In the project top directory, do

    python3 -m venv virtualenv
    source virtualenv/bin/activate
    pip install numpy # needed because of broken asap3 dependencies
    pip install -e .

to create a virtual environment, activate it and install a development
mode Salsa Dancing Molecules in it. If successful, the program can now
be run with

    salsa-dancing-molecules

which will run the current source code straight from the project
folder.

The installation only needs to be done once and during future
development sessions, it is enough to issue

    source virtualenv/bin/activate

from the project's top directory to enter the development environment.

## Running on Sigma Supercomputer
When multiple materials need to be studied, its recommended to run it on a supercomputer. This software is able to run on NSC:s supercomputer Sigma in Linköping, Sweden. The following link explains how to get started with Sigma: 

	https://www.nsc.liu.se/support/systems/sigma-getting-started/


In the project top directory, do

    module load Anaconda/2021.05-nsc1
    conda create -n salsa-dancing-molecules
    conda activate salsa-dancing-molecules
    conda install pip
    conda install -c conda-forge numpy asap3 openkim-models kim-api kimpy ase mpi4py
    pip install -e .


and answer yes to all questions to create an environment called
salsa_dancing_molecules, activate it and install Salsa Dancing
Molecules in development mode into it. If successful, the program can
be run with

    salsa-dancing-molecules

which will run the current source code straight from the project.

The installation step only needs to be done once and during future
development sessions, it is enough to issue

    conda activate salsa-dancing-molecules

to enter the development environment.

To run a generated sbatch script, do

    sbatch *filename*

to run the job on Sigma.

## Running the tests

To run the project's unit tests, first install pytest in the virtual
environment

	pip install pytest

then run

	pytest

from the top directory.

# Available commands
The different types of commands in the system are: 

	run: Runs the MD on argon
	nve: Runs a NVE simulation
	plot: Plots the simualtion data
	worker: Arguments for workers
	startup: Script for generating the neccessary files to run the program
	post_simulation: run post simulation calculation
	volume_process: run post volume-simulation calculation
	
For more information regarding each command and their positional - or optional arguments use help flags. An example of this is the following

	salsa-dancing-molecules run -h

where the ouput of this command will generating all the neccessary information regarding the command. 
# How to fill in the config file
An example with documentation to the config file can be found in ...\Salsa-Dancing-Molecules\example_simulation\example.conf. A description of each argument is given below:

material

	 Arg:    Mandatory
	 Type:   List or string
	 Desc:   Materials to be simulated. If using custom materials, the names shall 
	 correspond to atoms object(s) in the python file(s). If using materials project,use the 
	 prefix "mp_" followed by the formula to be searched for. Note, that "mp_element" will 
	 grab every type of that specific element and "mp_mp-id" will only grab that specific 
	 id.

materials_path

	Arg:    Optional
	Type:   String
	Desc:   The path where the materials are stored. Note: change the '/path/to/' to the 
	selected path directory. Otherwise the 'startup' command won't work. [materials] can be 
	either a folder with python files or a python file.

workspace_path

	Arg:    Mandatory
	Type:   String
	Desc:   The selected path of the workspace. Note: if no example_workspace exist, a 
	example_workspace will be created.

ensemble

	Arg:    Mandatory
	Type:   String or list of strings
	Desc:   The ensemble/ensembles for the selected materials. If single then string, if
	many then a list.

potential

	Arg:    Mandatory
	Type:   String or list of strings
	Desc:   Type of potential to be used on the materials.
kim-model

	Arg:    Mandatory if potential is openkim, otherwise optional.
	Type:   String or list of strings
	Desc:   The string is selected from openkim. This string is generated by selecting
	the specific material in the periodic table from: https://openkim.org/

initial-temperature

	Arg:    Mandatory
	Type:   Float or list of floats
	Desc:   The intial temperature of the simulation.

target-temperature

	Arg:    Mandatory if ensemble is NVT, otherwise optional
	Type:   Float or list of floats
	Desc:   The target temperature of the simulation.

repeat

	Arg:    Mandatory
	Type:   Integer or list of integers
	Desc:   The cellsize (generated by repeated sized of a single unitcell) of the 
	simulation. Example, if repeat=0 then simulating a unitcell.

steps

	Arg:    Mandatory
	Type:   Integer or list of integers
	Desc:   Number of timesteps for the simulation, 1 timestep=1fs
use-asap

	Arg:    Mandatory
	Type:   Boolean or list of booleans
	Desc:   True if the user want to use Asap, otherwise False
volume-scale

	Arg:    Optional
	Type:   Syntax, a,b: float and c: integer
	Desc:   A uniformed interval, [a-b, a+b], is generated with c: number of uniformly 
	spaced samples. The volume-scale scales the volume by a factor. If factor is 1: no 
	change in volume, if  <1: volume decreases and if  >1: volume decreases. 
pbc

	Arg:    Optional
	Type:   Boolean or list of booleans
	Desc:   True if the user wants to use periodic boundary conditions, otherwise False. If 
	no value is given, True will be used.

	



# Tutorials
This section provides some different tutorials of how to run the program. 

## Simple argon example
To run a simple argon example with a cell size of [5,5,5] in 1000 femtoseconds and with the outfile called simulation_data. Then you have to write the following,

	salsa-dancing-molecules run 1000 simulation_data
then a trajceory file will be created named simulation_data.traj containing all the trajectories during the simualtion and the data about the material propertires will be stored in a file called simualtion_data.csv. 

For help write: 
	
	salsa-dancing-molecules run -h

## Visualisation of data
Let the file containing the material properties from a simulation be named simulation_data.csv. To visualise the data generated from the simulation, do the following,

	salsa-dancing-molecules plot simulation_data.csv 
then it will plot three plots: the kintetic energy against potential energy, the temperature and the pressure. The plots will be saved in a image file called Image.png. 
If you want to generate a plot from the terminal then write:

	salsa-dancing-molecules plot simulation_data.csv --show
	
If you want to investigate a single specific property of the simulation: Ekin, Epot, Temp or Press. You write the follwoing:

	salsa-dancing-molecules plot simulation_data.csv singleImage.png Ekin --show

For help write: 
	
	salsa-dancing-molecules plot -h

## Running a simulation on the supercomputer
Suppose that the configuration file contains the information about the materials of interest. In this example, X is the api-key for the materials (you can generate the key by logging in to: https://materialsproject.org/ ) and simulation_config.conf is the configuration file. To create the necessary files for the supercomputer write the following: 

	salsa-dancing-molecules startup --api-key X --time 05:00:00 simulation_config.conf 
	
Then write: 

	sbatch run_workers.q

And the batch job will be submitted to the supercomputer. Data on the material properties will be saved in the folder done_simulations. 

For help write: 
	
	salsa-dancing-molecules startup -h
	
## OPTIMADE

It is possible to export simulation results as OPTIMADE compatible
json using the command line interface.

First post process the data, below is an example where
`/var/tmp/argon_workspace` contains simulation results from a
simulation using argon.

	salsa-dancing-molecules post_simulation /var/tmp/argon_workspace

NOTE: It is also possible to run `volume_process` if simulations with
      varying volumes have been performed.

This generates the file

	/var/tmp/argon_workspace/post_process_output/post_process_20-12-22_15_35_16.csv

containing all calculated values. To convert these results to OPTIMADE
compatible json, do the following

	salsa-dancing-molecules optimade /var/tmp/argon_workspace /var/tmp/argon_workspace/post_process_output/post_process_20-12-22_15_35_16.csv

where the first argument to the optimade command is the path to the
workspace and the second argument is the path to the datafile you wish
to process. By default, the output will be available as
`structures.json` in the current working directory.

Importing the data into Mongodb can then be performed by doing

	mongoimport --jsonArray --db optimade --collection structures --file structures.json

which imports the data into a database called optimade and a
collection called structures. See
https://github.com/Salsa-Dancing-Molecules/optimade-python-tools for
how to serve the data from the database.
