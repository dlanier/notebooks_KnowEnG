# KnowEnG's Signature Analysis Pipeline Notebook.
 --- 

This is the Knowledge Engine for Genomics (KnowEnG), an NIH BD2K Center of Excellence, Signature Analysis Pipeline.

This pipeline performs network-based **signature analysis** on the columns of a given spreadsheet, where spreadsheet's columns correspond to sample-labels and rows correspond to gene-labels.  The signature is based on correlating gene expression data (network enriched) against known gene signature data.

There are four similarity "signature"  methods that one can choose from:

- similarity        (traditional method) 
- net_similarity    (with network enrichment)
- cc_similarity     (with bootstraps)
- cc_net_similarity (with bootstraps and network enrichment)


and two correlation measures:
- spearman 
- cosine 

## _notebooks_KnowEnG_ Installation.
 ---

### First install the _Signature Analysis Pipeline_:
[Signature Analysis Pipeline Readme.md on github](https://github.com/KnowEnG-Research/Signature_Analysis_Pipeline/blob/master/README.md)

### Then install _notebooks_KnowEnG_:
[notebooks_KnowEnG Readme.md on github](https://github.com/dlanier/notebooks_KnowEnG/blob/master/README.md)

## Run  _Signature_Analysis_Pipeline_notebook.ipynb_

### If your browser allows auto-initialization you will see this screen.
<p align="center">
  <img  src="../data/images/SigA_Init.png" height=220>
</p>

### If not, and the code is showing, use the _Cell_ menu to _Run All_

<p align="center">
  <img  src="../data/images/SigA_UnInit.png" height=220>
</p>

### Click on the **View** button to see the selected run_parameters file.
<p align="center">
  <img  src="../data/images/SigA_View_Yaml.png" height=220>
</p>

### Click the **Run** button and the pipeline runs with the selected yaml file run_parameters.
<p align="center">
  <img  src="../data/images/SigA_View_Output.png" height=220>
</p>

### Use _Kernel_ menu _Restart and Clear Output_ to clear error messages (and all dispalyed output).
<p align="center">
  <img  src="../data/images/restart_notebook.png" height=320>
</p>
 

## Upload, view and transform your data:
 ---

### Use the _File_ menu _Open_ . 
<p align="center">
  <img  src="../data/images/file_open.png" height=320>
</p>

#### Select the _user_data_ directory.
<p align="center">
  <img  src="../data/images/user_data.png" height=220>
</p>

#### Click the _upload_ button to browse your computers files.
<p align="center">
  <img  src="../data/images/upload_button.png" height=320>
</p>

#### Click the highlighted _upload_ button begin the upload.
<p align="center">
  <img  src="../data/images/upload_button_2.png" height=120>
</p>

#### The file will appear in alphabetical order when the upload is complete.
<p align="center">
  <img  src="../data/images/upload_button_3.png" height=120>
</p>

## 3) Rename, download or delete your result files in the _results_ directory.
<p align="center">
  <img  src="../data/images/rename_download_or_delete.png" height=220>
</p>
