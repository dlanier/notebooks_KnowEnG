import os
import pandas as pd
from pandas.io.common import EmptyDataError

from IPython.display import display, HTML
import ipywidgets as widgets

import knpackage.toolbox as kn

"""                         Directory Structure setup  - code requires "results_dir" and "input_data_dir" """
USER_BASE_DIRECTORY = os.getcwd()
USER_DATA_DIRECTORY = os.path.join(USER_BASE_DIRECTORY, 'user_data')
USER_RESULTS_DIRECTORY = os.path.join(USER_BASE_DIRECTORY, 'results')

USER_BASE_DIRECTORIES_LIST = []
for maybe_dir in os.listdir(USER_BASE_DIRECTORY):
    maybe_dir_full = os.path.join(USER_BASE_DIRECTORY, maybe_dir)
    if os.path.isdir(maybe_dir_full):
        USER_BASE_DIRECTORIES_LIST.append(maybe_dir_full)

if len(USER_BASE_DIRECTORIES_LIST) < 1 or not USER_DATA_DIRECTORY in USER_BASE_DIRECTORIES_LIST:
    os.mkdir(USER_DATA_DIRECTORY)

if len(USER_BASE_DIRECTORIES_LIST) < 1 or not USER_RESULTS_DIRECTORY in USER_BASE_DIRECTORIES_LIST:
    os.mkdir(USER_RESULTS_DIRECTORY)


#                                                                                       file select constants
USER_DATAFILE_EXTENSIONS_LIST = ['.tsv', '.txt', '.df', '.gz']
LIST_BOX_UPDATE_MESSAGE = 'View == Update List'
BUTTON_CLEAR_STRING = 'Clear'
VIEW_FILE_STRING = 'View'


#                                                                                       layout styles
lisbox_layout                  = widgets.Layout(width='50%')

box_layout                     = widgets.Layout(display='inline-flex',
                                                flex_flow='row',
                                                justify_content='space-between',
                                                align_items='stretch',
                                                border='none',
                                                width='100%')

right_buttons_style_box_layout = widgets.Layout(display='flex',
                                                flex_flow='row',
                                                justify_content='flex-end',
                                                width='100%')

left_buttons_style_box_layout  = widgets.Layout(display='flex',
                                                flex_flow='row',
                                                justify_content='flex-start',
                                                width='100%')

labels_style_layout            = widgets.Layout(display='flex',
                                                flex_flow='row',
                                                justify_content='flex-end',
                                                width='20%')


#                                                                                   display with layout styles
def show_select_view_button(button):
    """ display file selector widget and view button """
    display(widgets.Box([button.file_selector, button], layout=box_layout))
    display(button.view_box)


def show_execute_button(button):
    """ show one button on the right with an ouput view box below """
    display(widgets.HBox([button], layout=right_buttons_style_box_layout))
    display(button.view_box)


def show_cell_title(title_string):
    """ display title string as html heading
    Args:
        title_string:    a python string type
    """
    title_string = "<h2>" + title_string + "</h2>"
    display(widgets.HTML(title_string))


def show_widget_right(one_widget):
    """ right justify widget  """
    display(widgets.HBox([one_widget], layout=right_buttons_style_box_layout))


def show_widget_left(one_widget):
    """ left justify widget """
    display(widgets.HBox([one_widget], layout=left_buttons_style_box_layout))


def show_select_view(list_box, view_button):
    """ standard layout for files list box and view button """
    display(widgets.Box([list_box, view_button], layout=box_layout))


def user_data_list(data_directory, file_types_list, include_update=True):
    """ user_file_list = update_user_data_list(user_data_dir, file_types_list)
    Args:
        target_dir:         valid directory name
        file_types_list:    list of file extensions - types e.g. ['.tsv', '.txt']

    Returns:
        types_file_list:    list of file names
    """
    types_file_list = []
    if os.path.isdir(data_directory) != True:
        return types_file_list

    for f in os.listdir(data_directory):
        if os.path.isfile(os.path.join(data_directory, f)):
            noNeed, f_ext = os.path.splitext(f)
            if f_ext in file_types_list:
                types_file_list.append(f)

    if len(types_file_list) <= 0:
        types_file_list.append('No Data')

    if include_update == True:
        types_file_list.append(LIST_BOX_UPDATE_MESSAGE)

    return types_file_list


def get_dropdown_files_listbox(data_directory=USER_DATA_DIRECTORY, file_types=USER_DATAFILE_EXTENSIONS_LIST):
    """ user_data dropdown listbox
    
    Returns: 
        files_dropdown_stock_box:  IPywidgets.Dropdown listbox with contents of user_data as options.
    """
    files_dropdown_stock_box = widgets.Dropdown(
        options=user_data_list(data_directory, file_types),
        description='',
        layout=lisbox_layout,
    )
    files_dropdown_stock_box.data_directory = data_directory
    files_dropdown_stock_box.file_types_list = file_types

    return files_dropdown_stock_box


def refresh_files_list(button):
    """ refresh files list """
    current_value = button.file_selector.value
    button.file_selector.options = user_data_list(button.file_selector.data_directory,
                                                  button.file_selector.file_types_list)
    if current_value in button.file_selector.options and current_value != LIST_BOX_UPDATE_MESSAGE:
        button.file_selector.value = current_value
    elif len(button.file_selector.options) > 0:
        button.file_selector.value = button.file_selector.options[0]


def get_view_box():
    """ empty HTML display area (one for each view button and output) """
    vb = widgets.HTML(
        value="",
        description="")
    return vb

def clear_view_box(view_box):
    """ clear values in widgets.HTML box """
    view_box.value = ''
    view_box.description = ''


def visualize_changed_file(change):
    """ show changed file selection
    Args:

    """
    select_file_listbox = change['owner']
    button = select_file_listbox.control_button

    if select_file_listbox.value == LIST_BOX_UPDATE_MESSAGE or select_file_listbox.value == '':
        clear_view_box(button.view_box)
        button.description = button.original_description
        refresh_files_list(button)
        return

    if button.description == BUTTON_CLEAR_STRING:
        button.description = VIEW_FILE_STRING
        if len(select_file_listbox.file_types_list) == 1 and '.yml' in select_file_listbox.file_types_list:
            visualize_selected_yaml_file(button)
        else:
            visualize_selected_file(button)
        button.description = BUTTON_CLEAR_STRING

        return


def visualize_selected_file(button):
    """ view button and output display callback

    Args:
        button:     IPywidgets.Button object containing an
                    IPywidgets.Dropdown (.file_selector)
                    with selected file name in .value
    """
    if hasattr(button, 'fname_list') == False and button.file_selector.value == LIST_BOX_UPDATE_MESSAGE:
            if button.description == BUTTON_CLEAR_STRING:
                clear_view_box(button.view_box)
                button.description = button.original_description

            refresh_files_list(button)
            return

    if button.description == BUTTON_CLEAR_STRING:
        clear_view_box(button.view_box)
        button.description = button.original_description
        return
    else:
        button.original_description = button.description
        button.description = BUTTON_CLEAR_STRING

    try:
        if hasattr(button, 'fname_list') == True:
            full_fname_list = button.fname_list
            S = ''
            for full_fname in full_fname_list:
                df = pd.read_csv(full_fname, sep='\t', header=0, index_col=0)
                path_not, f_name = os.path.split(full_fname)
                if hasattr(button, 'view_full_file') == True and button.view_full_file == True:
                    S = S + str(df.shape) + '    ' + f_name + df.to_html()
                else:
                    Step = df.iloc[0:10, 0:10]
                    S = S + str(df.shape) + '    ' + f_name + Step.to_html()
            button.view_box.value = S
        else:
            full_fname = os.path.join(button.file_selector.data_directory, button.file_selector.value)
            df = pd.read_csv(full_fname, sep='\t', header=0, index_col=0)
            if hasattr(button, 'view_full_file') == True and button.view_full_file == True:
                button.view_box.value = df.to_html()
                button.view_box.description = str(df.shape)
            else:
                Step = df.iloc[0:10, 0:10]
                button.view_box.value = Step.to_html()
                button.view_box.description = str(df.shape)

    except OSError:
        button.view_box.value = "No input data! "

    except EmptyDataError:
        button.view_box.value = "Empty input data! "

    except:
        button.view_box.value = "Invalid input data "


def visualize_selected_yaml_file(button):
    """ callback for yaml file view / clear button """
    if button.file_selector.value == LIST_BOX_UPDATE_MESSAGE:
        if button.description == BUTTON_CLEAR_STRING:
            clear_view_box(button.view_box)
            button.description = VIEW_FILE_STRING
        refresh_files_list(button)
        return

    if button.description == BUTTON_CLEAR_STRING:
        clear_view_box(button.view_box)
        button.description = VIEW_FILE_STRING
    else:
        yaml_files_directory = button.file_selector.data_directory
        yaml_file_name = button.file_selector.value
        button.view_box.value = get_run_parameters_string(yaml_files_directory, yaml_file_name)
        button.description = BUTTON_CLEAR_STRING


def get_run_parameters_string(run_files_path, yaml_file_name):
    """ construct a string from the run parameters """
    run_parameters = kn.get_run_parameters(run_files_path, yaml_file_name)
    S = '<p>'
    for k, v in run_parameters.items():
        S += '%25s : %s'%(k, v) + '<br>'
    S += '</p>'
    return S


def get_select_view_file_button_set(data_directory,
                                    button_name=VIEW_FILE_STRING,
                                    file_types_list=USER_DATAFILE_EXTENSIONS_LIST):
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

    select_file_button.file_selector.control_button = select_file_button
    select_file_button.file_selector.observe(visualize_changed_file, names='value')

    if len(file_types_list) == 1 and '.yml' in file_types_list:
        select_file_button.on_click(visualize_selected_yaml_file)
    else:
        select_file_button.on_click(visualize_selected_file)

    return  select_file_button

def get_single_file_execute_button(input_data_dir, results_dir, file_selector, button_name='run'):
    """ get an execute - view button for a single input file - callback set after return """
    single_file_execute_button = widgets.Button(
        description=button_name,
        disabled=False,
        button_style='',
        tooltip='execute selected file')
    single_file_execute_button.original_description = button_name

    single_file_execute_button.input_data_directory = input_data_dir
    single_file_execute_button.results_directory = results_dir
    single_file_execute_button.view_box = get_view_box()
    single_file_execute_button.file_selector = file_selector  # transpose_flistbx

    return single_file_execute_button


def get_two_files_execute_button(input_data_dir, results_dir, file_select_dict, button_name='run'):
    """ get an execute - view button for multiple files - callback set after return """
    two_files_execute_button = widgets.Button(
        description=button_name,
        disabled=False,
        button_style='',
        tooltip='execute selected file')

    two_files_execute_button.input_data_directory = input_data_dir
    two_files_execute_button.results_directory = results_dir
    two_files_execute_button.view_box = get_view_box()

    two_files_execute_button.file_1_selector = file_select_dict['file_1_selector']
    two_files_execute_button.file_2_selector = file_select_dict['file_2_selector']

    return two_files_execute_button
