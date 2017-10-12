FROM knowengdev/base_image:07_11_2017
MAINTAINER Dan Lanier <lanier4@illinois.edu>

ENV SRC_LOC /home

# Install the latest knpackage
RUN pip3 install -I knpackage dispy
RUN pip3 install --upgrade pip
RUN pip3 install jupyter

# Clone from github
RUN git clone https://github.com/dlanier/notebooks_KnowEnG.git ${SRC_LOC} 

# Set up working directory
WORKDIR ${SRC_LOC}

# locally use the current tag:
# docker run -v `pwd`:/home/test/run_dir -it -p 8888:8888 knowengdev/notebooks_knoweng:10_12_2017 jupyter notebook --ip 0.0.0.0 --no-browser --allow-root