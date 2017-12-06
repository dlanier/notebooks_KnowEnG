"""
lanier4@illinois.edu
Spreadsheeets_Transformation_notebook_tools.py
"""
import sys
import numpy as np

from knpackage import toolbox as kn

sys.path.insert(1, '../../notebooks_KnowEnG/src')

from layout_notebooks import *

sys.path.insert(1, '../Spreadsheets_Transformation/src')
import spreadsheets_transformation_toolbox as stt


DEFAULT_INPUT_FILES = {'transpose': 'transpose_spreadsheet.tsv',
                       'common_samples_1': 'intersect_spreadsheet_A.tsv',
                       'common_samples_2': 'intersect_spreadsheet_B.tsv',
                       'merge_1': 'merge_spreadsheet_A.txt',
                       'merge_2': 'merge_spreadsheet_B.txt',
                       'select_rows_spreadsheet': 'select_rows_spreadsheet.tsv',
                       'select_rows_list': 'select_rows_list.txt',
                       'select_averages_spreadsheet': 'average_spreadsheet.tsv',
                       'select_averages_dict': 'average_labels.tsv',
                       'select_categorical_spreadsheet': 'select_phenotype_spreadsheet.df',
                       'select_categorical_phenotype': 'select_phenotype_phenotype.txt',
                       'numerical_spreadsheet': 'other_transforms_spreadsheet.tsv',
                       'stats_spreadsheet': 'descriptive_statistic_spreadsheet.tsv',
                      }

def transpose_selected_file(button):
    """ callback for the transpose_execute_button

    Args:
        button:         an ipywidgets.Button object with an ipywidgets.Dropdown (.file_selector) object containing
                        the selected file name as its .value field.
    """
    if button.description == 'Clear':
        visualize_selected_file(button)
        return

    input_data_directory = button.input_data_directory
    input_file_name = button.file_selector.value
    spreadsheet_T_df = stt.transpose_df(
        kn.get_spreadsheet_df(
            os.path.join(input_data_directory, input_file_name)
        ))

    results_directory = button.results_directory
    transform_name = "transpose"
    result_file_name = stt.get_outfile_name(
        results_directory,
        input_file_name,
        transform_name,
        timestamp=False,
    )
    spreadsheet_T_df.to_csv(result_file_name, sep='\t', float_format='%g')

    button.fname_list = [result_file_name]
    visualize_selected_file(button)


def show_transpose_controls():
    show_cell_title('Transpose')
    # def get_select_view_file_button_set(data_directory,
    #                                 button_name=VIEW_FILE_STRING,
    #                                 file_types_list=USER_DATAFILE_EXTENSIONS_LIST):
    # """ get a view button with file select listbox and a file view box """
    get_transpose_file_button = get_select_view_file_button_set(data_directory=USER_DATA_DIRECTORY,
                                                                button_name=VIEW_FILE_STRING,
                                                                file_types_list=USER_DATAFILE_EXTENSIONS_LIST)
    if os.path.isfile(os.path.join(USER_DATA_DIRECTORY, DEFAULT_INPUT_FILES['transpose'])):
        get_transpose_file_button.file_selector.value \
            = DEFAULT_INPUT_FILES['transpose']

    transpose_execute_button = get_single_file_execute_button(
        USER_DATA_DIRECTORY,
        USER_RESULTS_DIRECTORY,
        file_selector=get_transpose_file_button.file_selector,
        button_name='Transpose',
    )
    transpose_execute_button.on_click(transpose_selected_file)

    show_select_view_button(get_transpose_file_button)

    show_execute_button(transpose_execute_button)



#                       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<0><0>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~>>
def select_numerical_transform(button):
    """ callback for get_numerical_function_execute_button

    Args:
        button:         an ipywidgets.Button object with 2 ipywidgets.Dropdown (.file_selector) objects containing
                        the selected file names in the .value fields.
    """
    if button.description == 'Clear':
        visualize_selected_file(button)
        return

    input_data_directory            = button.input_data_directory
    input_file_name                 = button.file_selector.value
    spreadsheet_df                  = kn.get_spreadsheet_df(os.path.join(input_data_directory, input_file_name))

    numeric_function                = button.numerical_function.value
    results_directory               = button.results_directory
    transform_name                  = numeric_function

    if transform_name == 'abs':
        result_df                   = stt.abs_df(spreadsheet_df)

    elif transform_name == 'z_transform':
        z_transform_axis            = button.numerical_function.z_transform_axis.value
        z_transform_ddof            = button.numerical_function.z_transform_ddof.value
        result_df                   = stt.z_transform_df(
            spreadsheet_df,
            axis=z_transform_axis,
            ddof=z_transform_ddof,
        )

    elif transform_name == 'log_transform':
        log_transform_log_base      = button.numerical_function.log_transform_log_base.value
        if log_transform_log_base == "e":
            log_transform_log_base  = np.exp(1)
        log_transform_log_offset    = button.numerical_function.log_transform_log_offset.value
        result_df                   = stt.log_transform_df(spreadsheet_df,
                                                           log_base=log_transform_log_base,
                                                           log_offset=log_transform_log_offset,
                                                           )

    elif transform_name == 'threshold':
        threshold_cut_off               = button.numerical_function.threshold_cut_off.value
        threshold_substitution_value    = button.numerical_function.threshold_substitution_value.value
        threshold_scope                 = button.numerical_function.threshold_scope.value
        result_df                       = stt.threshold_df(spreadsheet_df,
                                                           cut_off=threshold_cut_off,
                                                           sub_val=threshold_substitution_value,
                                                           scope=threshold_scope,
                                                           )

    result_file_name = stt.get_outfile_name(results_directory, input_file_name, transform_name, timestamp=False)
    result_df.to_csv(result_file_name, sep='\t',float_format='%g')
    button.fname_list = [result_file_name]
    visualize_selected_file(button)

""" display a numeric function options listbox and if selected is:
    abs             - grey out all else in all cases
    z_transform     - show radio button row or columns, and a int text box for ddof
    log_transform   - show log_transform float base text box, and a float offset box
    threshold       - show a float threshold cut-off, substitution box, and threshold bound [SUB_BELOW, SUB_ABOVE]
"""
def reset_aux_controls(change):
    """ callback - sub controls setup for numerical_transform method options """
    if change.old == 'z_transform':
        change['owner'].z_transform_axis.disabled=True
        change['owner'].z_transform_ddof.disabled=True

    elif change.old == 'log_transform':
        change['owner'].log_transform_log_base.disabled=True
        change['owner'].log_transform_log_offset.disabled=True

    elif change.old == 'threshold':
        change['owner'].threshold_cut_off.disabled=True
        change['owner'].threshold_substitution_value.disabled=True
        change['owner'].threshold_scope.disabled=True

    if change.new == 'abs':
        pass

    elif change.new == 'z_transform':
        change['owner'].z_transform_axis.disabled=False
        change['owner'].z_transform_ddof.disabled=False

    elif change.new == 'log_transform':
        change['owner'].log_transform_log_base.disabled=False
        change['owner'].log_transform_log_offset.disabled=False

    elif change.new == 'threshold':
        change['owner'].threshold_cut_off.disabled=False
        change['owner'].threshold_substitution_value.disabled=False
        change['owner'].threshold_scope.disabled=False

def show_numerical_transform_controls():
    show_cell_title('Other Transformations')

    # get the control widgets
    get_other_transform_file_button         = get_select_view_file_button_set(USER_DATA_DIRECTORY)
    if os.path.isfile(os.path.join(USER_DATA_DIRECTORY, DEFAULT_INPUT_FILES['numerical_spreadsheet'])):
        get_other_transform_file_button.file_selector.value = DEFAULT_INPUT_FILES['numerical_spreadsheet']

    numerical_function_options                          = ['abs', 'z_transform', 'log_transform', 'threshold']
    numerical_function_dropdown                         = widgets.Dropdown(
        options=numerical_function_options,
        value=numerical_function_options[0],
        description='stats function')

    threshold_scope                                          = ['SUB_BELOW', 'SUB_ABOVE']
    log_trans_base                                           = np.exp(1)
    default_threshold                                        = 0.5
    numerical_function_dropdown.z_transform_axis             = widgets.Dropdown(
        options={'rows': 0, 'columns': 1},
        value=0, description='axis',
        disabled=True)
    numerical_function_dropdown.z_transform_ddof             = widgets.IntText(
        value=0,
        description='ddof',
        disabled=True)
    numerical_function_dropdown.log_transform_log_base       = widgets.FloatText(
        value=log_trans_base,
        description='log_base',
        disabled=True)
    numerical_function_dropdown.log_transform_log_offset     = widgets.FloatText(
        value=0,
        description='offset',
        disabled=True)
    numerical_function_dropdown.threshold_cut_off            = widgets.FloatText(
        value=default_threshold,
        description='cut-off',
        disabled=True)
    numerical_function_dropdown.threshold_substitution_value = widgets.FloatText(
        value=0,
        description='substitute',
        disabled=True)
    numerical_function_dropdown.threshold_scope              = widgets.Dropdown(
        options=threshold_scope,
        value=threshold_scope[0],
        description='sub', disabled=True)
    numerical_function_dropdown.observe(reset_aux_controls, names='value')

    get_numerical_function_execute_button = get_single_file_execute_button(
        USER_DATA_DIRECTORY,
        USER_RESULTS_DIRECTORY,
        file_selector=get_other_transform_file_button.file_selector,
        button_name='Calculate',
    )
    get_numerical_function_execute_button.numerical_function = numerical_function_dropdown
    get_numerical_function_execute_button.on_click(select_numerical_transform)

    # display control widgets
    show_select_view_button(get_other_transform_file_button)
    show_widget_left(numerical_function_dropdown)
    show_widget_left(widgets.VBox([
        numerical_function_dropdown.z_transform_axis,
        numerical_function_dropdown.z_transform_ddof,
        numerical_function_dropdown.log_transform_log_base,
        numerical_function_dropdown.log_transform_log_offset,
        numerical_function_dropdown.threshold_cut_off,
        numerical_function_dropdown.threshold_substitution_value,
        numerical_function_dropdown.threshold_scope,
    ]))
    show_execute_button(get_numerical_function_execute_button)


def get_stats_value(button):
    """ callback for get_stats_execute_button

    Args:
        button:         an ipywidgets.Button object with 2 ipywidgets.Dropdown (.file_selector) objects containing
                        the selected file names in the .value fields.
    """
    if button.description == 'Clear':
        visualize_selected_file(button)
        return

    input_data_directory                        = button.input_data_directory
    input_file_name                             = button.file_selector.value
    spreadsheet_df                              = kn.get_spreadsheet_df(
        os.path.join(input_data_directory, input_file_name)
    )
    stats_function                              = button.stats_function.value
    direction_reference                         = button.direction_reference.value

    result_df                                   = stt.stats_df(
        spreadsheet_df,
        stats_function,
        direction_reference,
    )
    results_directory                           = button.results_directory
    stats_function                              = button.stats_function.value
    direction_reference                         = button.direction_reference.value
    transform_name                              = stats_function + '_' + direction_reference

    result_file_name                            = stt.get_outfile_name(
        results_directory,
        input_file_name,
        transform_name,
        timestamp=False,
    )
    result_df.to_csv(result_file_name, sep='\t',float_format='%g')

    button.fname_list                           = [result_file_name]
    visualize_selected_file(button)

def show_stats_value_controls():
    show_cell_title('Descriptive Statistics')
    # get the control widgets
    get_stats_function_file_button                  = get_select_view_file_button_set(USER_DATA_DIRECTORY)

    if os.path.isfile(os.path.join(USER_DATA_DIRECTORY, DEFAULT_INPUT_FILES['stats_spreadsheet'])):
        get_stats_function_file_button.file_selector.value \
            = DEFAULT_INPUT_FILES['stats_spreadsheet']

    stats_function_options                          = {
        'min': 'min',
        'max': 'max',
        'mean': 'mean',
        'median': 'median',
        'variance': 'variation',
        'std_deviation': 'std_deviation',
        'sum': 'sum',
    }

    stats_function_dropdown                         = widgets.Dropdown(
        options=stats_function_options,
        value=stats_function_options['min'],
        description='function',
    )

    direction_reference_options                     = ['columns', 'rows', 'all']
    direction_reference_dropdown                    = widgets.Dropdown(
        options=direction_reference_options,
        value=direction_reference_options[0],
        description='direction',
    )

    get_stats_execute_button                        = get_single_file_execute_button(
        USER_DATA_DIRECTORY,
        USER_RESULTS_DIRECTORY,
        file_selector=get_stats_function_file_button.file_selector,
        button_name='Calculate',
    )
    get_stats_execute_button.stats_function         = stats_function_dropdown
    get_stats_execute_button.direction_reference    = direction_reference_dropdown
    get_stats_execute_button.on_click(get_stats_value)

    # display control widgets
    show_select_view_button(get_stats_function_file_button)
    show_widget_left(widgets.VBox([stats_function_dropdown, direction_reference_dropdown]))
    show_execute_button(get_stats_execute_button)



