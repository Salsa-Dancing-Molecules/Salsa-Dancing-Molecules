"""Unit test for generate_json.py."""
import pytest
import os
from ..startup import generate_json


def test_config_to_configs():
    """Inputs example config and checks if returned config is correct."""
    in_dict = {"test1": ["1", "2", "3"],
               "test2": "string",
               "test3": ["one_item"],
               "test4": ["A", "B"]}
    expected_out_list = [{"test1": "1",
                          "test2": "string",
                          "test3": "one_item",
                          "test4": "A"},
                         {"test1": "1",
                          "test2": "string",
                          "test3": "one_item",
                          "test4": "B"},
                         {"test1": "2",
                          "test2": "string",
                          "test3": "one_item",
                          "test4": "A"},
                         {"test1": "2",
                          "test2": "string",
                          "test3": "one_item",
                          "test4": "B"},
                         {"test1": "3",
                          "test2": "string",
                          "test3": "one_item",
                          "test4": "A"},
                         {"test1": "3",
                          "test2": "string",
                          "test3": "one_item",
                          "test4": "B"}, ]
    generated_out_list = generate_json.config_to_configs(in_dict)
    assert generated_out_list == expected_out_list


def test_convert_to_json():
    """Checks if .json files are generated, does not check content."""
    in_dict = {"material": ["value"], "workspace_path": "./test"}
    generate_json.convert_to_json(in_dict)
    filename = "./test/unbegun_simulations/value.json"
    assert os.path.exists(filename)
    os.remove(filename)
