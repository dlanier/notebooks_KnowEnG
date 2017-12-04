"""
lanier4@illinois.edu
Spreadsheeets_Transformation_notebook_tools.py
"""
import sys

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

