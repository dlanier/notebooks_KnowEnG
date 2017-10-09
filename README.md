# Developing tools for KnowEnG's Pipelines 
This is the Knowledge Engine for Genomics (KnowEnG), an NIH BD2K Center of Excellence, Pipelines Notebooks.

There are four jupyter notebooks that one can choose from:

| **Notebook**                                      | **Pipeline**                        | **Parameters** |
| ------------------------------------------------ | -------------------------------------| -------------- |
| gene_prioritization_notebook                     | Gene_Prioritization_Pipeline         | eight parameter files |
| geneset_characterization_notebook                | GeneSet_Prioritization_Pipeline      | three parameter files|
| samples_clustering_notebook                      | Samples_Clustering_Pipeline          | eight parameter files|
| spreadsheets_transformation_notebook             | Spreadsheets_Transformation          | eight parameter files|

* * * 
## How to run these notebooks with Our data
* * * 
### 1. Clone the Samples_Clustering_Pipeline Repo
```
 git clone https://github.com/dlanier/notebooks_KnowEnG.git
```
 
### 2. Install the following (Ubuntu or Linux)
  ```
 pip3 install pyyaml
 pip3 install knpackage
 pip3 install scipy==0.18.0
 pip3 install numpy==1.11.1
 pip3 install pandas==0.18.1
 pip3 install matplotlib==1.4.2
 pip3 install scikit-learn==0.17.1
 
 apt-get install -y python3-pip
 apt-get install -y libfreetype6-dev libxft-dev
 apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran
```

### 3. Install jupyter notebook. http://jupyter.readthedocs.io/en/latest/install.html

```
pip3 install --upgrade pip

pip3 install jupyter
```

### 4. Start Jupyter

```
jupyter notebook
```

### 5. Start your notebook

```

```
