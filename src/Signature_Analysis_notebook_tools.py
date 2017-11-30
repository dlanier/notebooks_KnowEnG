""" Signature_Analysis_notebook_tools.py """
import os
import sys
import pandas as pd
from pandas.io.common import EmptyDataError

from IPython.display import display, HTML
import ipywidgets as widgets

import knpackage.toolbox as kn

lisbox_layout = widgets.Layout(width='50%')

box_layout = widgets.Layout(display='inline-flex',
                            flex_flow='row',
                            justify_content='space-between',
                            align_items='stretch',
                            border='none',
                            width='100%')

right_buttons_style_box_layout = widgets.Layout(display='flex',
                                                flex_flow='row',
                                                justify_content='flex-end',
                                                width='100%')

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

def visualize_selected_file(button):
    """ view button and output display callback
    
    Args:
        button:     IPywidgets.Button object containing an 
                    IPywidgets.Dropdown (.file_selector)
                    with selected file name in .value
    """
    if button.description == 'Clear':
        button.view_box.value = ''
        button.view_box.description = ''
        button.description = button.original_description
        return
    else:
        button.original_description = button.description
        button.description = 'Clear'

    try:
        if hasattr(button, 'fname_list') == True: 
            full_fname_list = button.fname_list
            S = ''
            for full_fname in full_fname_list: 
                df = pd.read_csv(full_fname,sep='\t',header=0,index_col=0)
                path_not, f_name = os.path.split(full_fname)
                if hasattr(button, 'view_full_file') == True and button.view_full_file == True:
                    S = S + str(df.shape) + '    ' + f_name + df.to_html()
                else:
                    Step = df.iloc[0:10,0:10];
                    S = S + str(df.shape) + '    ' + f_name + Step.to_html()
            button.view_box.value = S
        else: 
            full_fname = os.path.join(button.file_selector.data_directory, button.file_selector.value)
            df = pd.read_csv(full_fname, sep='\t', header=0, index_col=0)
            if hasattr(button, 'view_full_file') == True and button.view_full_file == True:
                button.view_box.value = df.to_html()
                button.view_box.description=str(df.shape)                
            else:
                Step = df.iloc[0:10,0:10];
                button.view_box.value = Step.to_html()
                button.view_box.description=str(df.shape)
        
    except OSError:
        button.view_box.value = "No input data! "
        
    except EmptyDataError:
        button.view_box.value = "Empty input data! "
        
    except:
        button.view_box.value = "Invalid input data "


def user_data_list(data_directory, file_types_list):
    """ user_file_list = update_user_data_list(user_data_dir, FEXT)
    Args:
        target_dir:     directory to list
        FEXT:           File extension list e.g. ['.tsv', '.txt']
    """
    my_file_list = []
    for f in os.listdir(data_directory):
        if os.path.isfile(os.path.join(data_directory, f)):
            noNeed, f_ext = os.path.splitext(f)
            if f_ext in file_types_list:
                my_file_list.append(f)
                
    if len(my_file_list) <= 0:
        my_file_list.append('No Data')
        
    return my_file_list

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

def refresh_files_list(button):
    """ refresh files list """
    current_value = button.file_selector.value
    button.file_selector.options = user_data_list(button.file_selector.data_directory, 
                                                  button.file_selector.file_types_list)
    if current_value in button.file_selector.options:
        button.file_selector.value = current_value
    
def get_select_view_file_button_set(data_directory, button_name='View', file_types_list=['.tsv','.txt','.df','.gz']):
    """ get a view button with file select listbox and a file view box """
    refresh_files_button = widgets.Button(description='Refresh',
                                           disabled=False,
                                           button_style='',
                                           tooltip='refresh files list')
    select_file_button = widgets.Button(description=button_name,
                                           disabled=False,
                                           button_style='',
                                           tooltip='visualize selected file')

    select_file_button.view_box = get_view_box()
    select_file_button.file_selector = get_dropdown_files_listbox(data_directory, file_types_list)
    select_file_button.file_selector.data_directory = data_directory
    select_file_button.file_selector.file_types_list = file_types_list
    if '.yml' in file_types_list:
        select_file_button.on_click(visualize_selected_yaml_file)
    else:
        select_file_button.on_click(visualize_selected_file)
        
    
    refresh_files_button.file_selector = select_file_button.file_selector
    
    refresh_files_button.on_click(refresh_files_list)
    
    select_file_button.refresh_files_button = refresh_files_button

    return  select_file_button

def show_select_view_button(button):
    """ formatted display of file selector button """
    display(widgets.Box([button.file_selector, button.refresh_files_button, button], layout=box_layout))
    display(button.view_box)
    
def get_single_file_execute_button(input_data_dir, results_dir, file_selector, button_name='run'):
    """ get an execute - view button for a single input file - callback set after return """
    single_file_execute_button = widgets.Button(
        description=button_name,
        disabled=False,
        button_style='',
        tooltip='execute selected file')

    single_file_execute_button.input_data_directory = input_data_dir
    single_file_execute_button.results_directory = results_dir
    single_file_execute_button.view_box = get_view_box()
    single_file_execute_button.file_selector = file_selector

    return single_file_execute_button

def show_execute_button(button):
    """ formatted display of execute button """
    display(widgets.HBox([button], layout=right_buttons_style_box_layout))
    display(button.view_box)

def visualize_selected_yaml_file(button):
    """ callback for yaml file view / clear button """
    if button.description == 'Clear':
        button.view_box.value = ''
        button.description = 'View'
    else:
        yaml_files_directory = button.file_selector.data_directory
        yaml_file_name = button.file_selector.value
        button.view_box.value = get_run_parameters_string(yaml_files_directory, yaml_file_name)
        button.description = 'Clear'
    
    
def get_run_parameters_string(run_files_path, yaml_file_name):
    """ construct a string from the run parameters """
    run_parameters = kn.get_run_parameters(run_files_path, yaml_file_name)
    S = '<p>'
    for k, v in run_parameters.items():
        S += '%25s : %s'%(k, v) + '<br>'
    S += '</p>'
    return S

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
    """ construct and show the signature analysis pipeline select and run widgets """
    select_file_button = get_select_view_file_button_set(run_directory, button_name='View', file_types_list=['.yml'])
    show_select_view_button(select_file_button)
    exbutton = get_single_file_execute_button(run_directory, 
                                              results_dir, 
                                              select_file_button.file_selector, 
                                              button_name='RUN')
    exbutton.on_click(execute_yaml_file)
    show_execute_button(exbutton)
    
def show_results_dir_button():
    """ refreshable button to show results directory """
    get_results_file_button = get_select_view_file_button_set(results_dir)
    show_select_view_button(get_results_file_button)
        