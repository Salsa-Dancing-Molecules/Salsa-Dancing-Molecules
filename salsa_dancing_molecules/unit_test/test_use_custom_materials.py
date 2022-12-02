"""Unit test for use_custom_materials.py."""
import pytest
import os
from ..startup import use_custom_materials


def test_materials_to_pickles():
    """Inputs test atoms object and checks if pickle file is created."""
    path_to_atoms_object = ("salsa_dancing_molecules/unit_test/" +
                            "example_material.py")
    work_path = "salsa_dancing_molecules/unit_test"
    material_names = ["gold_fcc"]
    use_custom_materials.materials_to_pickles(path_to_atoms_object,
                                              work_path,
                                              material_names)
    filename = ("salsa_dancing_molecules/unit_test/"
                "materials/gold_fcc.pickle")
    assert os.path.exists(filename)
    os.remove(filename)
