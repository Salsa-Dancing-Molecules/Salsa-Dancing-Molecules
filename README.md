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
