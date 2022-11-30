"""Module converts the configurations into a Json-files."""
import json


def config_to_configs(config):
    """Generate all combinations of elements from dict with lists.

    Args:
        config - dictionary to be used as template.
    Returns:
        list_of_json_dicts - list of all the different new dictionaries.
    """
    list_of_json_dicts = []
    for key in config.keys():
        if type(config[key]) is list:
            if len(list_of_json_dicts) == 0:
                for new_item in config[key]:
                    list_of_json_dicts.append({key: new_item})
            else:
                new_list = []
                for json_dict in list_of_json_dicts:
                    for new_item in config[key]:
                        new_dict = {}
                        for old_key, old_value in json_dict.items():
                            new_dict[old_key] = old_value
                        new_dict[key] = new_item
                        new_list.append(new_dict)
                list_of_json_dicts = new_list
        else:
            for json_dict in list_of_json_dicts:
                json_dict[key] = config[key]
    return list_of_json_dicts


def convert_to_json(config):
    """Generate a json file for each configuration set.

    The function takes in a dictionary to be used as a template
    describing the different types of simulations to be run.
    Then, multiple json files are generated, one for each specific simulation.
    Args:
        config - dictionary to be used as template.
    """
    list_of_dicts = config_to_configs(config)
    for json_dict in list_of_dicts:
        name_string = ""
        for key, value in json_dict.items():
            if not (key == "materials_path" or key == "workspace_path"):
                name_string += value+'_'
        name_string = name_string.lstrip('_')
        json_dict["material"] = (json_dict["workspace_path"] +
                                 "/materials/" +
                                 json_dict["material"] +
                                 ".pickle")
        with open(json_dict["workspace_path"] +
                  "/unbegun_simulations/" +
                  name_string+".json", "w") as outfile:
            json.dump(json_dict, outfile)
