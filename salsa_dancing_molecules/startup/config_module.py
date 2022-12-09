"""Module containing configuration functions."""
import configparser
import numpy as np


def string_to_list(s):
    """Convert a string into a list.

    Args:
        s - string describing a list
    Returns:
        list if s described a list, otherwise returns s
    """
    if s.startswith('[') and s.endswith(']'):
        return s.strip('][').split(',')
    elif s.startswith('(') and s.endswith(')'):
        values = [x.strip() for x in s.strip(')(').split(',')]
        start = float(values[0])-float(values[1])
        stop = float(values[0])+float(values[1])
        result_list = np.around(np.linspace(start, stop, int(values[2])), 4)
        return [str(x) for x in result_list]
    return s


def read_configuration(filename):
    """Open file and create config.

    Args:
        filename - path to file with config.
    Returns:
        config - dictionary with strings and lists.

    Example config can be found in example_simulation/simulation_config.conf.
    The resulting dictionary has values that also are dictionaries.
    Those dictionaries have values that are only strings, before some of those
    strings are converted to lists with strings.
    """
    con = configparser.ConfigParser()
    con.read(filename)
    config = con._sections
    for section in config.keys():
        for key in config[section].keys():
            config[section][key] = string_to_list(config[section][key])
    return config
