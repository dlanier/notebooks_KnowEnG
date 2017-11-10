# SCRIPT = ../src/spreadsheets_transformation_pipelines.py
RUN_DIR = ./run_dir
RUN_FILES = ../data/run_files
NB_FILES = ../data/notebooks
RESULTS_DIR = $(RUN_DIR)/results
INPUT_DATA_DIR = ../data
UNIT_TEST_TEMP_DIR = ./unit/tmp

RMR = rm -rf
MKDIR_P = mkdir -p

# ----------------------------------------------------------------
# Benchmarks setup Section                                       -
# ----------------------------------------------------------------
env_setup: create_run_dir copy_run_files

create_run_dir:
	$(MKDIR_P) $(RESULTS_DIR) 

copy_run_files:
	cp $(RUN_FILES)/*.yml $(RUN_DIR); cp $(NB_FILES)/*.ipynb .

clean_dir_recursively:
	$(RMR) $(RUN_DIR)