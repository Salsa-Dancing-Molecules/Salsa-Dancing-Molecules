"""This is a setuptools based installation script."""

from setuptools import setup, find_packages

setup(
    name="Salsa-Dancing-Molecules",
    version="0.0.1",
    description="A molecular dynamics simulation software",
    url="https://github.com/Salsa-Dancing-Molecules/Salsa-Dancing-Molecules",
    classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(where="."),
    python_requires=">=3.7",
    install_requires=['ase', 'asap3'],
    entry_points={
        "console_scripts": [
            "salsa-dancing-molecules=salsa_dancing_molecules:main",
        ],
    },
)
