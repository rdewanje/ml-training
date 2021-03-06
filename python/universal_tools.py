'''Universal tools for file IO and other
'''
import shutil
import csv
import itertools
import json
import os
import numpy as np
import glob
from sklearn.metrics import confusion_matrix


def best_to_file(best_values, output_dir, assesment):
    '''Saves the best parameters and the scores to a file
    'best_parameters.json'

    Parameters:
    ----------
    best_values : dict
        Best parameters found during the evolutionary algorithm
    output_dir : str
        Directory where best parameters and assessment is saved
    assessment : dict
        Different scores for the best parameters found for both train and test
        dataset.
    '''
    output_path = os.path.join(output_dir, 'best_hyperparameters.json')
    with open(output_path, 'w') as file:
        json.dump(best_values, file)
        file.write('\n')
        json.dump(assesment, file)


def save_dict_to_json(dictionary, output_path):
    '''Saves the feature importances into a feature_importances.json file

    Parameters:
    ----------
    dictionary : dict
        Dicotionay to be saved
    output_dir : str
        Path to the output file

    Returns:
    -------
    Nothing
    '''
    with open(output_path, 'w') as file:
        json.dump(dictionary, file)


def save_run_settings(output_dir):
    '''Saves the run settings for future reference

    Parameters:
    ----------
    output_dir : str
        Path to the output directory

    Returns:
    -------
    Nothing
    '''
    settings_dir = os.path.join(output_dir, 'run_settings')
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
    wild_card_path = os.path.join(
        os.path.expandvars('$CMSSW_BASE'),
        'src/machineLearning/machineLearning/settings/*'
    )
    for path in glob.glob(wild_card_path):
        shutil.copy(path, settings_dir)


def read_parameters(param_file):
    '''Read values form a '.json' file

    Parameters:
    ----------
    param_file : str
        Path to the '.json' file

    Returns:
    -------
    value_dicts : list containing dicts
        List of parameter dictionaries
    '''
    value_dicts = []
    with open(param_file, 'rt') as file:
        for line in file:
            json_dict = json.loads(line)
            value_dicts.append(json_dict)
    return value_dicts



def to_one_dict(list_of_dicts):
    '''Puts dictionaries from list into one big dictionary. (can't have same
    keys)

    Parameters:
    ----------
    list_of_dicts : list of dicts
        List filled with dictionaries to be put together into one big dict

    Returns:
    -------
    main_dict : dict
        Dictionary containing all the small dictionary keys.
    '''
    main_dict = {}
    for elem in list_of_dicts:
        key = list(elem.keys())[0]
        main_dict[key] = elem[key]
    return main_dict


def read_settings(settings_dir, group):
    '''Function to read the global settings of the optimization

    Parameters:
    -----------
    group : str
        Group of settings wanted. Either: 'global', 'ga' or 'pso'

    Returns:
    --------
    settings_dict : dict
        Dictionary containing the settings for the optimization
    '''
    settings_path = os.path.join(
        settings_dir,
        group + '_settings.json')
    settings_dict = read_multiline_json_to_dict(settings_path)
    return settings_dict


def read_multiline_json_to_dict(file_path):
    '''Reads multiline .json file to one dictionary

    Parameters:
    ----------
    file_path : str
        Path to the .json file

    Returns:
    -------
    json_dict : dict
        Dictionary created from the multiline .json file
    '''
    parameter_list = read_parameters(file_path)
    json_dict = to_one_dict(parameter_list)
    return json_dict