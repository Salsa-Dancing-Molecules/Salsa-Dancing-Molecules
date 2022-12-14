"""OPTIMADE models for describing simulation results."""
from optimade.models import EntryResource, EntryResourceAttributes
from optimade.models.utils import (
        StrictField,
        SupportLevel,
        OptimadeField,
)
from typing import Optional


class SimulationResultAttributes(EntryResourceAttributes):
    """Represents the calculated values of a simulation."""

    _salsa_msd_average: Optional[float] = OptimadeField(
        ...,
        description="""The average mean square displacement
given as a float.""",
        support=SupportLevel.MUST,
        queryable=SupportLevel.MUST)

    _salsa_self_diffusion_coefficient: Optional[float] = OptimadeField(
            ...,
            description="""The self diffusion coefficient given as a float.""",
            support=SupportLevel.MUST,
            queryable=SupportLevel.MUST)

    _salsa_heat_capacity: Optional[float] = OptimadeField(
            ...,
            description="""The heat capacity given as a float.""",
            support=SupportLevel.MUST,
            queryable=SupportLevel.MUST)

    _salsa_debye_temperature: Optional[float] = OptimadeField(
            ...,
            description="""The debye temperature given as a float.""",
            support=SupportLevel.MUST,
            queryable=SupportLevel.MUST)

    _salsa_cohesive_energy: Optional[float] = OptimadeField(
            ...,
            description="""The cohesive energy given as a float.""",
            support=SupportLevel.MUST,
            queryable=SupportLevel.MUST)

    _salsa_equilibrium_warning: Optional[str] = OptimadeField(
            ...,
            description="""Provides a warning if the equilibrium
might not have been reached.""",
            support=SupportLevel.OPTIONAL,
            queryable=SupportLevel.MUST)

    _salsa_debye_warning: Optional[str] = OptimadeField(
            ...,
            description="""Provides a warning if the debye
temperature might not be reliable.""",
            support=SupportLevel.OPTIONAL,
            queryable=SupportLevel.MUST)


class SimulationResult(EntryResource):
    """Represents the result of a simulation."""

    type: str = StrictField(
            "calculations",
            description="The name of the type of an entry.",
            regex="^calculations$",
            support=SupportLevel.MUST,
            queryable=SupportLevel.MUST,
    )

    attributes: SimulationResultAttributes
