"""Unit tests for the materialsproject module."""
import pytest
import uuid

from os import remove
from os.path import exists

from ..materialsproject import MatClient


# This custom mock class is needed because the unittest mock class can
# not be pickled.
class Atom:
    """Mock atom class."""

    def __init__(self, formula):
        """Init the mock atom with a chemical formula."""
        self.formula = formula

    def get_chemical_formula(self):
        """Return a mocked chemical formula."""
        return self.formula


class TestPickle:
    """Test the pickle functionality of MatClient."""

    def setup_class(self):
        """Initialise the tests."""
        self.client = MatClient('a' * 32)
        self.atom = Atom(uuid.uuid4())

    def test_collision_without_id(self):
        """Test colliding when no ID is requested."""
        # Pickle the same atom twice and check if we get two files.
        success0, name0 = self.client._pickle(self.atom, '.')
        assert success0
        assert name0 == f'{self.atom.get_chemical_formula()}.pickle'
        assert exists(name0)

        success1, name1 = self.client._pickle(self.atom, '.')
        assert success1
        assert name1 == f'{self.atom.get_chemical_formula()}-0.pickle'
        assert exists(name1)

        remove(name0)
        remove(name1)

    def test_collision_with_id(self):
        """Test colliding when an ID is requested."""
        # Create pickle with ID 0
        success0, name0 = self.client._pickle(self.atom, '.', 0)
        assert success0
        assert name0 == f'{self.atom.get_chemical_formula()}-0.pickle'
        assert exists(name0)

        # Creating a pickle with the same name should fail.
        success1, _ = self.client._pickle(self.atom, '.', 0)
        assert not success1

        # Creating a pickle with a new ID should succeed.
        success2, name2 = self.client._pickle(self.atom, '.', 1)
        assert success2
        assert name2 == f'{self.atom.get_chemical_formula()}-1.pickle'
        assert exists(name2)

        remove(name0)
        remove(name2)
