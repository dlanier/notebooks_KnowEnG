"""
lanier4@illinois.edu
Spreadsheeets_Transformation_notebook_tools.py
"""
import sys
# sys.path.insert(1, '../notebooks_KnowEnG/src')
sys.path.insert(1, './')
from layout_notebooks import *

def show_transpose_controls():
    show_cell_title('Transpose')
    get_transpose_file_button = get_select_refresh_view_file_button(USER_DATA_DIRECTORY)
    # get_transpose_file_button.file_selector.observe(refresh_files_list)
    show_select_refresh_view_button(get_transpose_file_button)
