"""Module containing a mock-atoms class, used for testing pressure.py."""


class atoms:
    """This is a mock-class for atoms used for testing pressure.py."""

    def __len__(self):
        """Return mock-length."""
        return 3

    def get_volume(self):
        """Return mock-volume."""
        return 10

    def get_positions(self):
        """Return mock-positions."""
        return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def get_forces(self):
        """Return mock-forces."""
        return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def get_temperature(self):
        """Return mock-temperature."""
        return 273
