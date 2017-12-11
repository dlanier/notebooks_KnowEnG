"""
Copyright 2017 University of Illinois Board of Trustees. All Rights Reserved.
Licensed under the MIT  license (the "License");
You may not use this file except in compliance with the License.
The License is included in the distribution as License.txt file.
 
Software  distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and  limitations under the License.
"""
import os
import sys
# import pandas as pd
# from pandas.io.common import EmptyDataError
#
# # from IPython.display import display, HTML
# import ipywidgets as widgets

sys.path.insert(1, './')
from layout_notebooks import *

SIG_A_TYPES_LIST = ['.yml']
SIG_A_OUTPUT_TYPES_LIST = ['.tsv','.df']

run_directory = os.path.abspath('user_data')
main_file_path = os.path.abspath('../../../Signature_Analysis_Pipeline/src')
main_file = os.path.join(main_file_path,'gene_signature.py')
results_dir = os.path.abspath('results')


def disp_run_parameters(run_parameters):
    """ formateed display of the run_parameters dict """
    for k, v in run_parameters.items():
        print('%25s : %s'%(k, v))


def execute_yaml_file(button):
    """ call back for execute command line button """
    yaml_file_name = button.file_selector.value

    call_python_string = 'python3 ' + main_file + ' -run_directory ' + run_directory + ' -run_file ' + yaml_file_name

    os.system(call_python_string)


def show_Signatute_Analysis_Execute_button():
    """ construct and show the signature analysis pipeline select and run widgets
     get_select_refresh_view_file_button
    """
    select_file_button = get_select_view_file_button_set(run_directory, button_name='View', file_types_list=['.yml'])
    show_select_view_button(select_file_button)
    exbutton = get_single_file_execute_button(run_directory, 
                                              results_dir, 
                                              select_file_button.file_selector, 
                                              button_name='RUN')
    exbutton.on_click(execute_yaml_file)
    show_execute_button(exbutton)
    

def show_results_dir_button(results_dir):
    """ refreshable button to show results directory """
    get_results_file_button = get_select_view_file_button_set(results_dir,
                                                              button_name='View',
                                                              file_types_list=SIG_A_OUTPUT_TYPES_LIST)
    show_select_view_button(get_results_file_button)


def show_signature_analysis_controls():
    """  """
    show_Signatute_Analysis_Execute_button()
    show_results_dir_button(results_dir)
