"""
author: lanier4@illinois.edu
functions to convert yaml file data source and output directory references 
to local directory references using a python dict
"""
import os
import pandas as pd
import knpackage.toolbox as kn

def yaml_append(yaml_file_name_full_path, new_key, new_value):
    """ Usage:  yaml_append(yaml_file_name_full_path, new_key, new_value)  """
    if not os.path.isfile(yaml_file_name_full_path):
        print('file not found:\n', yaml_file_name_full_path)
        return
    
    appendable_text = '\n' + new_key + ':    ' + new_value + '\n'
    print(yaml_file_name_full_path)
    try:
        with open(yaml_file_name_full_path, "a+") as yaml_file:
            yaml_file.write(appendable_text)
    except:
        print('Not Properly Appended:\n', yaml_file_name_full_path)
        pass

def get_yaml_files_list(yaml_dir):
    """ yaml_files = get_yaml_files_list(YAML_DIR) """
    yaml_files = []
    for f in os.listdir(yaml_dir):
        if os.path.isfile(os.path.join(yaml_dir, f)) and f[-3:] == 'yml':
            yaml_files.append(f)
            
    return yaml_files

def display_yaml_files_list(yaml_dir):
    yaml_files = get_yaml_files_list(yaml_dir)
    print(yaml_dir)
    for f in yaml_files:
        print('\t',f)

def display_all_yaml_files(yaml_dir, yaml_files):
    n_files = len(yaml_files)
    count = 0
    for f in yaml_files:
        count += 1
        print('\n\n%30s : %s'%(f, yaml_dir))
        print('%30s : %s '%(' "file[' + str(count-1) + ']" :~) ' + str(count), 'of ' + str(n_files)))
        run_parameters = kn.get_run_parameters(yaml_dir, f)
        for k, v in run_parameters.items():
            print('%30s : %s'%(k,v))

def get_available_directory_names(dir_name):
    """ dir_names = get_available_directory_names(DIR_NAME) """
    if not os.path.isdir(dir_name):
        return []
    dir_names = []
    for maybe_dir in os.listdir(dir_name):
        if os.path.isdir(maybe_dir) and maybe_dir[0] != '.':
            dir_names.append(maybe_dir)

    return dir_names

"""
# Example dictionary
run_dir = os.getcwd()
local_dict = {'data/spreadsheets': SPREADSHEETS_DIR, 
              'data/networks': NETWORKS_DIR, 
              'run_dir' : run_dir, 
              'data/run_files' : YAML_DIR}
"""

def set_local_run_parameters(run_parameters, local_dict):
    """ run_parameters = set_local_run_parameters(run_parameters, local_dict) """
    for key_name, key_value in local_dict.items():
        for k, v in run_parameters.items():
            if 'full_path' in k or 'directory' in k:
                if key_name in v:
                    de_nada, f_name = os.path.split(v)
                    run_parameters[k] = os.path.join(key_value, f_name)
                
    return run_parameters


def get_parameter_keys_dict(yaml_dir, parameter_key_dict={}, methods_list=[]):
    """  get the list of yaml files in the yaml_dir, the list of methods in all those, and a dictionary of key types

    Args:
        yaml_dir:           path the the yaml files
        parameter_key_dict: (optional) dictionary to add key types
        methods_list:       (optional) list of methods to append

    Returns:
        yaml_files_list:    the list of yaml files in the yaml_dir
        methods_list:       the list of methods in the yaml files
        parameter_key_dict: key-name: key-type   dictionary
    """
    type_dict = {int: 'int', float: 'real', str: 'string', list: 'list'}

    yaml_files_list = []
    for f in os.listdir(yaml_dir):
        ff = os.path.join(yaml_dir, f)
        some_nombre, nombre_ext = os.path.splitext(f)
        if os.path.isfile(ff) and nombre_ext == '.yml':
            yaml_files_list.append(f)

    for f_name in yaml_files_list:
        run_parameters = kn.get_run_parameters(yaml_dir, f_name)
        for k, v in run_parameters.items():
            if k not in parameter_key_dict.keys():
                parameter_key_dict[k] = type_dict[type(v)]
            if k == 'method' and k not in methods_list:
                methods_list.append(v)

    methods_list = list(set(methods_list))
    return parameter_key_dict, methods_list, yaml_files_list


def get_yaml_df(yaml_dir, UNUSED_FILL='not used'):
    """ read the yaml files in 'yaml_dir' and constuct a datafrme with rows of keys, columns of file names and
        filled with the each yaml file values.
    Args:
        yaml_dir:       path the the yaml files
        UNUSED_FILL:    string to use for fill where a yaml file has no entry for a key (row name)
    """
    key_dict, methods_list, yaml_files_list = get_parameter_keys_dict(yaml_dir)
    if 'run_file' in key_dict.keys():
        key_dict.pop('run_file')
    yaml_file_df = pd.DataFrame(data=None, index=key_dict.keys(), columns=None)

    for f_name in yaml_files_list:
        run_parameters = kn.get_run_parameters(yaml_dir, f_name)
        if 'run_file' in run_parameters.keys():
            run_parameters.pop('run_file')

        yaml_file_df[f_name] = UNUSED_FILL
        for k, v in run_parameters.items():
            yaml_file_df[f_name].loc[k] = v

    return yaml_file_df

def get_key_value_df(par_df, key_name, key_value, null_string='not used'):
    """ get the dataframe where row 'key_name' values match 'key_value' """
    col_dict = (par_df.loc[key_name] == key_value).to_dict()
    col_list = []
    for k, v in col_dict.items():
        if v == True:
            col_list.append(k)

    if len(col_list) > 0:
        par_df = par_df[col_list]

    rows_used_list = []
    for row_name in par_df.index:
        if (par_df.loc[row_name].values == null_string).any() == False:
            rows_used_list.append(row_name)
    if len(rows_used_list) > 0:
        par_df = pd.DataFrame(par_df.loc[rows_used_list])

    return par_df

def get_methods_df_dict(yaml_dir):
    """ methods_df_dict = get_methods_df_dict(yaml_dir) """
    key_dict, methods_list, yaml_files_list = get_parameter_keys_dict(yaml_dir)
    run_parameters_df = get_yaml_df(yaml_dir)
    methods_df_dict = {}
    for method_name in methods_list:
        methods_df_dict[method_name + '_df'] = get_key_value_df(run_parameters_df, 'method', method_name)

    return methods_df_dict