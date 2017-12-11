# Developing tools for KnowEnG's Pipelines 
This is the Knowledge Engine for Genomics (KnowEnG), an NIH BD2K Center of Excellence, Pipelines Notebooks.

There are two jupyter notebooks that one can choose from:

| **Notebook**                                      | **Pipeline**                        | **Parameters** |
| ------------------------------------------------ | -------------------------------------| -------------- |
| Signature_Analysis_Pipeline_notebook             | Signature_Analysis_Pipeline          | Signature Analysis parameter files |
| Kaplan_Meier                                     | Independent notebook                 | notebook settings|

* * * 
## How to run these notebooks with Our data
* * * 
 
### 1. Install the following (Ubuntu or Linux)
  ```
 pip3 install pyyaml
 pip3 install xmlrunner
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

### 2. Install jupyter notebook. ( http://jupyter.readthedocs.io/en/latest/install.html )
```
pip3 install --upgrade pip

pip3 install jupyter
```

### 3. Clone these KnowEnG Repositories:
```
 git clone https://github.com/dlanier/notebooks_KnowEnG.git
 git clone https://github.com/KnowEnG/Signature_Analysis_Pipeline.git
```

### 4. In each Repository's test directory setup the environment.
```
 cd (clones location)/Signature_Analysis_Pipeline/test
 make env_setup
 cd ../../notebooks_KnowEnG/test/
 make env_setup
 cd run_dir
```

### 5. Start Jupyter
```
jupyter notebook
```

### 6. Click on a notebook to open it - see Graphical insructions for running the notebooks:
[Kaplan_Meier](https://github.com/dlanier/notebooks_KnowEnG/blob/master/docs/Kaplan_Meier.md)
[Signature_Analysis](https://github.com/dlanier/notebooks_KnowEnG/blob/master/docs/Signature_Analysis.md)
