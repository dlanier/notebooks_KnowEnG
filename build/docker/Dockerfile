FROM knowengdev/notebooks_knoweng:base_hub_11_10_2017
MAINTAINER Dan Lanier <lanier4@illinois.edu>
# build current image for notebooks.knoweng.org

ENV NB_SRC_LOC /home/notebooks_KnowEnG
RUN git clone https://github.com/dlanier/notebooks_KnowEnG.git ${NB_SRC_LOC} 

# Set up working directory
ENV SRC_LOC /home
WORKDIR ${SRC_LOC}


# docker run -v `pwd`:/home/admin_tank/beam_me_out_scotty -p 8000:8000 -it knowengdev/notebooks_knoweng:11_10_2017 jupyterhub --ip=0.0.0.0 --port=8000
