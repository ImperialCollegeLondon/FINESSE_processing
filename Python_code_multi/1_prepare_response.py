"""
This file will input raw data and then 
- Preparing individual interferograms
- Average 40 inteferograms
- Calculating response functions

It is based on code written by Laura Warwick ETC from 1_prepare and 2_calculate files
"""

# Importing functions
from glob import glob
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import calibration_functions_sanjee as cal

"Loading files here"
# Experimental data from FINESSE spec INPUTS
DATE = "20230220"
PATH = '/disk1/Andoya/sp1016/'
INT_LOCATION = PATH+ f"Raw_Data/{DATE}/"
# RUN NAME is the string at the end of the folder
RUN_NAME = "zenith_test1"

# GUI data files
GUI_DATA_LOCATION = INT_LOCATION + "clear_sky1-20230220103722.log"

# Saving outputs here!
PATH2 = '/disk1/sm4219/NEW_finesse_process_ouput/'
# The INDIVIDUAL_SAVE_LOCATION will be created if it does not already exist
INDIVIDUAL_SAVE_LOCATION = PATH2+f"Processed_Data_trial1/prepared_individual_ints/"
Path(INDIVIDUAL_SAVE_LOCATION).mkdir(parents=True, exist_ok=True)
SAVE_LOCATION = PATH2+f"Processed_Data_soph_single/"
gui_data = cal.load_gui(GUI_DATA_LOCATION)

FOLDERS = glob(INT_LOCATION + "*" + RUN_NAME + "/")
FOLDERS.sort()

