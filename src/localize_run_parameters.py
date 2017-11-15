"""
author: lanier4@illinois.edu
functions to convert yaml file data source and output directory references 
to local directory references using a python dict
"""
import os

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