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

# Using the KnowEnG Signature_Analysis_Pipeline_notebook.ipynb notebook.
 ---

### To run the notebook on your machine follow the directions to install the Signature Analysis Pipeline:
[Readme.md github](https://github.com/KnowEnG-Research/Signature_Analysis_Pipeline/blob/master/README.md)

### If your browser allows auto-initialization you will see this screen.
<p align="center">
  <img  src="../data/images/up_and_running.png" height=220>
</p>
