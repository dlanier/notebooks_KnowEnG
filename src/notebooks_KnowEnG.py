import os
import yaml
from IPython.display import display, HTML

from knpackage import toolbox as kn

def get_user_path_dict(pipelines_root_directory='/pipelines', user_notebooks_path='knoweng_pipelines'):
    """ default path setup to accomodate server or local running  """
    user_home = os.path.expanduser('~')
    user_path_dict = {}

    user_path_dict['pipelines_root_directory'] = os.path.abspath(pipelines_root_directory)

    # KnowEnG_notebooks_directory
    user_path_dict['notebooks_KnowEnG_directory'] = os.path.abspath(os.path.join(pipelines_root_directory, 'notebooks_KnowEnG'))

    user_path_dict['user_home'] = user_home
    user_path_dict['notebooks_home_directory'] = os.path.join(user_home, user_notebooks_path)
    user_path_dict['run_directory'] = os.path.join(user_path_dict['notebooks_home_directory'], 'test/run_dir')
    user_path_dict['notebook_results_directory'] = os.path.join(user_path_dict['notebooks_home_directory'], 'test/run_dir/results')

    # tmp_directory need not exist - just in user owned place
    user_path_dict['tmp_directory'] = os.path.join(user_path_dict['notebook_results_directory'], 'tmp')
    user_path_dict['skip_dirs']=['notebooks_KnowEnG']

    return user_path_dict


def run_dir_setup(user_notebooks_path='knoweng_pipelines', pipelines_root_directory='/pipelines'):
    """ make notebook default directories in user home """
    user_path_dict = get_user_path_dict(pipelines_root_directory, user_notebooks_path)
    notebook_results_directory = user_path_dict['notebook_results_directory']
    if not os.path.isdir(notebook_results_directory):
        os.makedirs(notebook_results_directory, exist_ok=True)


def setup_test_dir(notebook_location):
    notebook_results_directory = os.path.join(os.path.abspath(notebook_location),'test/run_dir/results')
    if not os.path.isdir(notebook_results_directory):
        os.makedirs(notebook_results_directory, exist_ok=True)


def display_run_parameters(run_parameters):
    """ notebook convenience """
    if isinstance(run_parameters, dict):
        for k, v in run_parameters.items():
            print('%30s : %s'%(k,str(v)))
    else:
        print('\n\t\trun_parameters are zippo\n')


def view_spreadsheet_file_head(full_file_name):
    """ notebook convenience """
    if os.path.isfile(full_file_name):
        sp_df = kn.get_spreadsheet_df(full_file_name)
        deNada, f_name = os.path.split(full_file_name)
        print(f_name , ' size:', sp_df.shape)
        display(sp_df.head(10))
    else:
        print('file not found on local path')


def copy_yaml_with_path_edit(pipeline_directory_full_path, run_directory, results_directory):
    """ copy and convert the yaml file relative paths to work in users run_directory """
    yaml_files_source_directory = os.path.join(pipeline_directory_full_path, 'data/run_files')
    if not os.path.isdir(yaml_files_source_directory):
        # do nothing if this pipeline has no yaml files
        return

    yaml_dir_list = os.listdir(yaml_files_source_directory)
    if len(yaml_dir_list) < 1:
        print('No files found in :\n\t', yaml_files_source_directory)
        return

    for maybe_yaml in yaml_dir_list:
        if len(maybe_yaml) > 4 and maybe_yaml[-4:] == '.yml':
            run_parameters = kn.get_run_parameters(yaml_files_source_directory, maybe_yaml)
            for k, v in run_parameters.items():
                if k == 'results_directory':
                    run_parameters['results_directory'] = results_directory
                elif k == 'tmp_directory':
                    run_parameters['tmp_directory'] = os.path.join(results_directory, 'tmp')
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


def copy_pipeline_yaml_files_to_user(pipelines_root_directory, skip_dirs):
    """ copy the all yaml files and modify the pathnames """
    user_path_dict = get_user_path_dict(pipelines_root_directory)

    pipeline_directory_names = os.listdir(pipelines_root_directory)
    for maybe_dir in pipeline_directory_names:
        if maybe_dir in skip_dirs:
            print('Skip Directory:', maybe_dir)
            pass
        else:
            pipeline_directory_full_path = os.path.join(pipelines_root_directory, maybe_dir)
            if os.path.isdir(pipeline_directory_full_path) == True:
                copy_yaml_with_path_edit(pipeline_directory_full_path,
                                         run_directory=user_path_dict['run_directory'],
                                         results_directory=user_path_dict['notebook_results_directory'])


def copy_notebooks_to_user(notebooks_from_directory, notebooks_to_directory):
    """ simple copy notebooks called from import_knoweng_pipeline_notebooks """
    for maybe_file in os.listdir(notebooks_from_directory):
        full_file_name = os.path.join(notebooks_from_directory, maybe_file)
        if os.path.isfile(full_file_name) and maybe_file[-6:] == '.ipynb':
            os.system('cp ' + full_file_name + ' ' + os.path.abspath(notebooks_to_directory))


def import_knoweng_pipeline_notebooks(pipelines_root_directory='/pipelines'):
    """ import the notebooks from notebooks_KnowEnG volume on server
    """
    user_path_dict = get_user_path_dict(pipelines_root_directory)
    #copy_pipeline_yaml_files_to_user(pipelines_root_directory=user_path_dict['pipelines_root_directory'],
    #                                 skip_dirs=user_path_dict['skip_dirs'])

    notebooks_from_directory=os.path.join(user_path_dict['notebooks_KnowEnG_directory'], 'data/notebooks')
    copy_notebooks_to_user(notebooks_from_directory=notebooks_from_directory,
                           notebooks_to_directory=user_path_dict['notebooks_home_directory'])
