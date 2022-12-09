"""Unittest for functions in config_module."""
import pytest
from ..startup.config_module import string_to_list, read_configuration


def test_string_to_list():
    """Function for testing string_to_list.py."""
    test_list_1 = "[1,34,324,25,34,5]"
    generated_val_1 = string_to_list(test_list_1)
    expected_val_1 = ['1', '34', '324', '25', '34', '5']

    test_list_2 = "(1,0.5,11)"
    generated_val_2 = string_to_list(test_list_2)
    expected_val_2 = ["0.5", "0.6", "0.7", "0.8", "0.9", "1.0", "1.1",
                      "1.2", "1.3", "1.4", "1.5"]

    assert (generated_val_1 == expected_val_1 and
            generated_val_2 == expected_val_2)


def test_read_configuration():
    """Function for testing read_configuration.py."""
    generated_dict = read_configuration('salsa_dancing_molecules' +
                                        '/unit_test/test_configuration.conf')
    expected_dict = {'Test': {'test': ['1', '2', '3'],
                     'test2': ['2', '4', '6'], 'test3': ['test']}}

    assert generated_dict == expected_dict
