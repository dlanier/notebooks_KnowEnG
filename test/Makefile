RUN_DIR = ./run_dir
SPREADSHEET_FILES = ../data/spreadsheets
NETWORK_FILES = ../data/networks
RUN_FILES = ../data/run_files
NOTEBOOK_FILES = ../src/notebook

RUN_DATA = $(RUN_DIR)/user_data
RESULTS_DIR = $(RUN_DIR)/results

RMR = rm -rf
MKDIR_P = mkdir -p

# ----------------------------------------------------------------
# notebooks setup Section                                       -
# ----------------------------------------------------------------
env_setup: create_run_dir copy_data_files  copy_run_files

create_run_dir:
	$(MKDIR_P) $(RESULTS_DIR); $(MKDIR_P) $(RUN_DATA)

copy_data_files:
	cp $(SPREADSHEET_FILES)/* $(RUN_DATA); cp $(NETWORK_FILES)/* $(RUN_DATA); cp $(RUN_FILES)/* $(RUN_DATA)

copy_run_files:
	cp $(NOTEBOOK_FILES)/*.ipynb $(RUN_DIR)

clean_dir_recursively:
	$(RMR) $(RUN_DIR)
