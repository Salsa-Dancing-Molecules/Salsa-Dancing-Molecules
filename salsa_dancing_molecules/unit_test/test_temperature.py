"""Unittest for temperature.py."""
import pytest
from ..temperature import get_temperature
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution


def test_temperature():
    """Test if the correct value is calculated after setting temp to 300K."""
    atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                              symbol='Cu',
                              size=(3, 3, 3), pbc=True)
    MaxwellBoltzmannDistribution(atoms, temperature_K=300)
    assert get_temperature(atoms) == pytest.approx(300, rel=1e-1)
