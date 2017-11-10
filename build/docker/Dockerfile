FROM knowengdev/base_image:09_19_2017
MAINTAINER Dan Lanier <lanier4@illinois.edu>
# build current image for notebooks.knoweng.org

ENV SRC_LOC /home

RUN pip3 install -I knpackage dispy
RUN pip3 install --upgrade pip
RUN pip3 install jupyter

RUN git clone https://github.com/dlanier/notebooks_KnowEnG.git ${SRC_LOC}

WORKDIR ${SRC_LOC}

# run locally:
# docker run -v `pwd`:/home/test/run_dir -it -p 8888:8888 knowengdev/notebooks_knoweng:10_12_2017 jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
