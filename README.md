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
    conda activate salsa_dancing_molecules
    conda install pip
    pip install numpy # needed because of broken asap3 dependencies
    pip install -e .

and answer yes to all questions to create an environment called
salsa_dancing_molecules, activate it and install Salsa Dancing
Molecules in development mode into it. If successful, the program can
be run with

    salsa-dancing-molecules

which will run the current source code straight from the project.

The installation step only needs to be done once and during future
development sessions, it is enough to issue

    conda activate salsa_dancing_molecules

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
