"""Variable class contains the relevant physical quantatives of system."""

from .pressure import get_pressure
from .energy import get_energy, get_kinetic_energy, get_potential_energy
from .temperature import get_temperature
from .filerwriter import file_saver
import numpy as np


class Variables:
    """Creates object of each variable."""

    def __init__(self):
        """Initialise an empty data collection."""
        self.potential_energies = []
        self.kinetic_energies = []
        self.atomic_pressures = []
        self.temperatures = []

        self.time = []
        self.timestep = 0
        self.time_counter = 0

    def Snapshot(self, a):
        """Take a snapshot of the state during the dynamics."""
        self.potential_energies.append(get_potential_energy(a))
        self.kinetic_energies.append(get_kinetic_energy(a))
        self.atomic_pressures.append(get_pressure(a))
        self.temperatures.append(get_temperature(a))

    def list_to_array(self):
        """Convert the global lists into arrays."""
        self.potential_energies = np.array(
            self.potential_energies, dtype=float)
        self.kinetic_energies = np.array(self.kinetic_energies, dtype=float)
        self.atomic_pressures = np.array(self.atomic_pressures, dtype=float)
        self.temperatures = np.array(self.temperatures, dtype=float)
        self.time = np.array(self.time, dtype=float)

    def generate_file(self, file_name='simulation_data.csv'):
        """Save the physical quantatives into a CSV file."""
        file_saver(
            output_path=file_name,
            data_head=['Potential Energy (eV)', 'Kinetic Energy (eV)',
                       'Pressure (Pa)', 'Temperature (K)', 'Time (fs)'],
            data_list=[self.potential_energies, self.kinetic_energies,
                       self.atomic_pressures, self.temperatures, self.time]
        )

    def set_timestep(self, step):
        """Set the timestep."""
        self.timestep = step

    def increment_time(self):
        """Time increment."""
        self.time.append(self.time_counter)
        self.time_counter = self.time_counter+self.timestep
