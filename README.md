# Salsa Dancing Molecules

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
