"""OPTIMADE models for describing simulation results."""
from optimade.models import (
    EntryResource,
    EntryResourceAttributes,
)
from optimade.models.utils import (
    StrictField,
    SupportLevel,
    OptimadeField,
)
from typing import Optional


class SimulationConfiguration(EntryResourceAttributes):
    """Represents the configuration used for a simulation."""

    ensemble: Optional[str] = OptimadeField(
            ...,
            description="""Ensemble in which the simulation is performed.""")

    potential: Optional[str] = OptimadeField(
            ...,
            description="""Potential used when simulating.""")

    kim_model: Optional[str] = OptimadeField(
            ...,
            description="""KIM model used when simulating if potential
is openkim.""")

    initial_temperature: Optional[int] = OptimadeField(
            ...,
            description="""The initial temperature of the material.""",
            unit="K")

    target_temperature: Optional[int] = OptimadeField(
            ...,
            description="""The target temperature of NVT.""",
            unit="K")

    volume_scale: Optional[float] = OptimadeField(
            ...,
            description="""Scale factor of the material.""")


class AggregateSimulationResultAttributes(SimulationConfiguration):
    """Represents the result from aggregated simulations."""

    lattice_constant: Optional[float] = OptimadeField(
            ...,
            description="""Lattice constant given as a float.""",
            unit="Å")

    bulk_modulus: Optional[float] = OptimadeField(
            ...,
            description="""Bulk modulus given as a float.""",
            unit="GPa")

    lindeman_criterion: Optional[str] = OptimadeField(
            ...,
            description="""True if the lindeman criterion > 0.1.""")


class SingleSimulationResultAttributes(SimulationConfiguration):
    """Represents the calculated values of a simulation."""

    msd_average: Optional[float] = OptimadeField(
        ...,
        description="""The average mean square displacement
given as a float.""",
        unit="Å^2")

    self_diffusion_coefficient: Optional[float] = OptimadeField(
            ...,
            description="""The self diffusion coefficient given as a float.""",
            unit="Å^2s^-1")

    heat_capacity: Optional[float] = OptimadeField(
            ...,
            description="""The heat capacity given as a float.""",
            unit="Jkg^-1K^-1")

    debye_temperature: Optional[float] = OptimadeField(
            ...,
            description="""The debye temperature given as a float.""",
            unit="K")

    cohesive_energy: Optional[float] = OptimadeField(
            ...,
            description="""The cohesive energy given as a float.""",
            unit="eV")

    equilibrium_warning: Optional[str] = OptimadeField(
            ...,
            description="""Provides a warning if the equilibrium
might not have been reached.""")

    debye_warning: Optional[str] = OptimadeField(
            ...,
            description="""Provides a warning if the debye
temperature might not be reliable.""")
