""" Signature_Analysis_notebook_tools.py """
import os
import sys
import pandas as pd
from pandas.io.common import EmptyDataError

# from IPython.display import display, HTML
import ipywidgets as widgets

sys.path.insert(1, './')
from layout_notebooks import *

SIG_A_TYPES_LIST = ['.yml']
SIG_A_OUTPUT_TYPES_LIST = ['.tsv','.df']

run_directory = os.path.abspath('user_data')
main_file_path = os.path.abspath('../Signature_Analysis_Pipeline/src')
main_file = os.path.join(main_file_path,'gene_signature.py')
results_dir = os.path.abspath('results')


def get_view_box():
    """ empty HTML display area (one for each view button and output) """
    vb = widgets.HTML(
        value="",
        description="")
    return vb


def get_dropdown_files_listbox(data_directory, file_types_list):
    """ user_data dropdown listbox
    
    Returns: 
        files_dropdown_stock_box:  IPywidgets.Dropdown listbox with contents of user_data as options.
    """
    files_dropdown_stock_box = widgets.Dropdown(
        options=user_data_list(data_directory, file_types_list),
        description='',
        layout=lisbox_layout,
    )
    return files_dropdown_stock_box


def get_select_view_file_button_set(data_directory, button_name='View', file_types_list=SIG_A_TYPES_LIST):
    """ get a view button with file select listbox and a file view box """
    select_file_button = widgets.Button(description=button_name,
                                           disabled=False,
                                           button_style='',
                                           tooltip='visualize selected file')
    select_file_button.original_description = button_name

    select_file_button.view_box = get_view_box()
    select_file_button.file_selector = get_dropdown_files_listbox(data_directory, file_types_list)
    select_file_button.file_selector.data_directory = data_directory
    select_file_button.file_selector.file_types_list = file_types_list

    if '.yml' in file_types_list:
        select_file_button.on_click(visualize_selected_yaml_file)
    else:
        select_file_button.on_click(visualize_selected_file)

    return  select_file_button


def disp_run_parameters(run_parameters):
    """ formateed display of the run_parameters dict """
    for k, v in run_parameters.items():
        print('%25s : %s'%(k, v))


def execute_yaml_file(button):
    """ call back for execute command line button """
    yaml_file_name = button.file_selector.value

    call_python_string = 'python3 ' + main_file + ' -run_directory ' + run_directory + ' -run_file ' + yaml_file_name

    os.system(call_python_string)


def show_signature_analysis_controls():
    show_Signatute_Analysis_Execute_button()
    show_results_dir_button(results_dir)


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
        
