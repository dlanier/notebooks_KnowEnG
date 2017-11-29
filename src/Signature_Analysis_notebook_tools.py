
import os
import sys

import knpackage.toolbox as kn

sys.path.insert(1, '../Signature_Analysis_Pipeline/src')
import gene_signature_toolbox as gsa_tbx

run_files_path = 'user_data/run_files'

def disp_run_parameters(run_parameters):
    """ formateed display of the run_parameters dict """
    for k, v in run_parameters.items():
        print('%25s : %s'%(k, v))


def run_yaml_file(yaml_file_name):
    if os.path.isfile(os.path.join(run_files_path, yaml_file_name)):
        print('file is found')
        run_parameters = kn.get_run_parameters(run_files_path, yaml_file_name)
        disp_run_parameters(run_parameters)
        
        if run_parameters['method'] == 'similarity':
            gsa_tbx.run_similarity(run_parameters)
        elif run_parameters['method'] == 'cc_similarity':
            gsa_tbx.run_cc_similarity(run_parameters)
        elif run_parameters['method'] == 'net_similarity':
            gsa_tbx.run_net_similarity(run_parameters)
        elif run_parameters['method'] == 'cc_net_similarity':
            gsa_tbx.run_cc_net_similarity(run_parameters)
        else:
            print('run_parameters method not found')