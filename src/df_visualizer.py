import os
import sys

import pandas as pd
from IPython.display import display, HTML
from ipywidgets import *

from knpackage import toolbox as kn

sys.path.insert(1, '../../notebooks_KnowEnG/src')
from layout_notebooks import *

df_style = '<style>tc, tr, th, td {padding: 5px; text-align: center; background-color: yellow;}</style>'
slider_big = '500px'
slider_small = '20px'

def view_box_display_control(button):
    """  """
    box_dict = button.dict
    if button.description == 'Clear':
        box_dict['view_box'].value = ''
        box_dict['vertical'].layout.height = slider_small
        button.description = 'Show'
    else:
        reset_view_box_display(box_dict)
        button.description = 'Clear'

def reset_view_box_display(box_dict):
    """ update dataframe view segment with slider values """
    v0 = min(box_dict['vertical'].value, box_dict['height'] - box_dict['vertical'].segment)
    v1 = min(box_dict['height'], v0 + box_dict['vertical'].segment)
    
    h0 = min(box_dict['horizontal'].value, box_dict['width'] - box_dict['horizontal'].segment)
    h1 = min(box_dict['width'], h0 + box_dict['horizontal'].segment)
    
    box_dict['view_box'].value = df_style + box_dict['df'].iloc[v0:v1, h0:h1].to_html()
    box_dict['vertical'].layout.height = slider_big
    
def df_slider(change):
    """ callback for row or column slider slider """
    box_dict = change['owner'].dict
    if box_dict['show_hide_button'].description == 'Clear':
        reset_view_box_display(box_dict)

    
def get_df_slider_view_box(df_file_name, heigth_segment=20, width_segment=10, do_display=True):
    """ open a (maybe big) dataframe, return a set of controls to view a chunk of it """
    df = kn.get_spreadsheet_df(df_file_name)
    box_dict = {'df': df}
    
    height = df.shape[0]
    heigth_segment = min(heigth_segment, height)
    width = df.shape[1]
    width_segment = min(width_segment, width)
    
    
    box_dict['view_box'] = get_view_box()
    box_dict['view_box'].value = df_style + df.iloc[0:heigth_segment, 0:width_segment].to_html()
    box_dict['height'] = height
    box_dict['width'] = width
    
    box_dict['dir_name'], box_dict['file_name'] = os.path.split(df_file_name)
    box_dict['df_label'] = Label(value='[%i, %i] - %s'%(box_dict['height'], box_dict['width'], box_dict['file_name']))
    
    box_dict['vertical'] = IntSlider(value=0,
                                    min=0,
                                    max=height,
                                    step=1,
                                    description='Row',
                                    disabled=False,
                                    continuous_update=False,
                                    orientation='vertical',
                                    readout=True,
                                    readout_format='d',
                                    layout=Layout(height=slider_big))
    box_dict['vertical'].segment = heigth_segment
    box_dict['vertical'].observe(df_slider, names='value')
    
    box_dict['horizontal'] = IntSlider(value=0,
                                        min=0,
                                        max=width,
                                        step=1,
                                        description='Colum',
                                        disabled=False,
                                        continuous_update=False,
                                        orientation='horizontal',
                                        readout=True,
                                        readout_format='d')
    box_dict['horizontal'].segment = width_segment
    box_dict['horizontal'].observe(df_slider, names='value')
    
    box_dict['show_hide_button'] = Button(description='Clear',
                                         disabled=False,
                                         button_style='')
    box_dict['show_hide_button'].on_click(view_box_display_control)
    
    box_dict['low_box'] = HBox([box_dict['vertical'], box_dict['view_box']])
    box_dict['top_box'] = HBox([box_dict['df_label'], box_dict['horizontal'], box_dict['show_hide_button']])
    box_dict['show_box'] = VBox([box_dict['top_box'], box_dict['low_box']])
    
    box_dict['show_hide_button'].dict = box_dict
    box_dict['vertical'].dict = box_dict
    box_dict['horizontal'].dict = box_dict
    if do_display == True:
        display(box_dict['show_box'])
    
    return box_dict