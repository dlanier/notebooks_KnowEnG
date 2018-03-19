# Check and create the local directory struct            RUN ONCE
import os
import sys
import yaml
from knpackage import toolbox as kn

# local environment definitions:
pipelines_root_directory = os.path.abspath('/pipelines')
notebooks_home_directory = 'notebooks/test' 
run_directory = 'notebooks/test/run_dir'
# tmp_directory need not exist - just in user owned place
notebook_results_directory = os.path.abspath('notebooks/test/run_dir/results')
tmp_directory = os.path.join(notebook_results_directory, 'tmp')

if not os.path.isdir(notebook_results_directory):
    os.makedirs(notebook_results_directory, exist_ok=True)

def display_run_parameters(run_parameters):
    if isinstance(run_parameters, dict):
        for k, v in run_parameters.items():
            print('%30s : %s'%(k,str(v)))
    else:
        print('\n\t\trun_parameters are zippo\n')
        
def copy_yaml_with_path_edit(pipeline_directory_full_path, run_directory, results_directory):
    yaml_files_source_directory = os.path.join(pipeline_directory_full_path, 'data/run_files')
    if not os.path.isdir(yaml_files_source_directory):
        # quit if this pipeline has no yaml files
        print(yaml_files_source_directory,'\n\t\t  DNE \n')
        return
    
    tmp_directory = os.path.join(results_directory, 'tmp')
    yaml_dir_list = os.listdir(yaml_files_source_directory)
    if len(yaml_dir_list) < 1:
        print('No files found in :\n\t', yaml_files_source_directory)
        return
    
    run_parameters_dict_list = []
    for maybe_yaml in yaml_dir_list:
        if len(maybe_yaml) > 4 and maybe_yaml[-4:] == '.yml':
            run_parameters = kn.get_run_parameters(yaml_files_source_directory, maybe_yaml)
            for k, v in run_parameters.items():
                if k == 'results_directory':
                    run_parameters['results_directory'] = notebook_results_directory
                elif k == 'tmp_directory':
                    run_parameters['tmp_directory'] = os.path.join(notebook_results_directory, 'tmp')
                elif k == 'run_directory':
                    run_parameters['run_directory'] = run_directory
                elif isinstance(v, str) and len(v) > 1 and v[0:2] == './':
                    path_string = v[2:]
                    run_parameters[k] = os.path.join(pipeline_directory_full_path, path_string)
                elif isinstance(v, str) and len(v) > 1 and v[0:3] == '../':
                    path_string = v[3:]
                    run_parameters[k] = os.path.join(pipeline_directory_full_path, path_string)
                    
            full_file_name = os.path.join(run_directory, maybe_yaml)
            try:
                with open(full_file_name, 'w') as fh:
                    yaml.dump(run_parameters, fh, default_flow_style=False)
            except Exception:
                print(full_file_name, '\n\t Exception Unknown')
                pass
            
def copy_pipeline_yaml_files_to_user(pipelines_root_directory, run_dir, results_dir, skip_dirs=['notebooks_KnowEnG']):
    pipeline_directory_names = os.listdir(pipelines_root_directory)
    for maybe_dir in pipeline_directory_names:
        if maybe_dir in skip_dirs:
            print('Skip Directory:', maybe_dir)
            pass
        else:
            pipeline_directory_full_path = os.path.join(pipelines_root_directory, maybe_dir)
            if os.path.isdir(pipeline_directory_full_path) == True:
                copy_yaml_with_path_edit(pipeline_directory_full_path, 
                                         run_directory=run_directory, 
                                         results_directory=notebook_results_directory)

def copy_notebooks_to_user(notebooks_from_directory, notebooks_to_directory):
    for maybe_file in os.listdir(notebooks_from_directory):
        full_file_name = os.path.join(notebooks_from_directory, maybe_file)
        if os.path.isfile(full_file_name) and maybe_file[-6:] == '.ipynb':
            os.system('cp ' + full_file_name + ' ' + os.path.abspath(notebooks_to_directory))

            

def import_knoweng_pipeline_notebooks():
#     user_base_dir = os.getcwd()

    copy_pipeline_yaml_files_to_user(pipelines_root_directory=pipelines_root_directory, 
                                    run_dir=run_directory, 
                                    results_dir=notebook_results_directory, 
                                    skip_dirs=['notebooks_KnowEnG'])

    KnowEnG_notebooks_directory = os.path.join(pipelines_root_directory, 'notebooks_KnowEnG/data/notebooks')
    copy_notebooks_to_user(notebooks_from_directory=KnowEnG_notebooks_directory, 
                           notebooks_to_directory=notebooks_home_directory)

    print('Hallelujah!')
    