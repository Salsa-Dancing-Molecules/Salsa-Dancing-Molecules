"""Module containing configuration functions."""
import configparser
import json


def read_configuration(filename, section='Gold'):
    con = configparser.ConfigParser()
    con.read(filename)
    materials_dict = {}
    for key in con.options(section):
        materials_dict[key] = con.get(section, key)
    return materials_dict


def generate_JSON(dictionary, output_directory):
    json_object = json.dumps(dictionary)
    with open(output_directory + dictionary['symbols']+'.json', 'w') as fp:
        json.dump(json_object, fp)
