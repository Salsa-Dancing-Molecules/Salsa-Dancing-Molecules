"""Module containing configuration functions."""
import configparser


def string_to_list(s):
    """Convert a string into a list.

    Args:
        s - string describing a list
    Returns:
        list if s described a list, otherwise returns s
    """
    if s.startswith('[') and s.endswith(']'):
        return s.strip('][').split(',')
    return s


def read_configuration(filename):
    """Open file and create config.

    Args:
        filename - path to file with config.
    Returns:
        config - dictionary with strings and lists.
    """
    con = configparser.ConfigParser()
    con.read(filename)
    config = con._sections
    for section in config.keys():
        for key in config[section].keys():
            config[section][key] = string_to_list(config[section][key])
    return config
