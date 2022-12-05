"""Unittest for functions in config_module."""
import pytest
from ..startup.config_module import string_to_list, read_configuration


def test_string_to_list():
    """Function for testing string_to_list.py."""
    test_list = "[1,34,324,25,34,5]"
    generated_val = string_to_list(test_list)
    expected_val = ['1', '34', '324', '25', '34', '5']

    assert generated_val == expected_val


def test_read_configuration():
    """Function for testing read_configuration.py."""
    generated_dict = read_configuration('salsa_dancing_molecules' +
                                        '/unit_test/test_configuration.conf')
    expected_dict = {'Test': {'test': ['1', '2', '3'],
                     'test2': ['2', '4', '6'], 'test3': ['test']}}

    assert generated_dict == expected_dict
