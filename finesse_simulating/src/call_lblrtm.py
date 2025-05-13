"""CALL_LBLRTM

Functions to run the LBLRTM executable and read TAPE12 output

"""

import panel_file as panpy
from module_function_list import *


# This class allows you to change the current working
# directory as you would in linux. IT is needed to run
# LBLRTM later on. You coud probably
# do this yourself using os if you prefered
class cd:
    """Context manager for changing the current working directory
    from https://stackoverflow.com/questions/431684/how-do-i-change-directory-cd-in-python/13197763#13197763
    """

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def call_lblrtm(lbl_location, save_location, OD):
    """Runs the LBLRTM executable

    Args:
        lbl_location (_path_): location of local LBLRTM exeutable
        sav_location (_path_): save location
        OD (_variable_): specifies if writing out seperate optical depth files
                           (0 = no, 1 = yes)
    """
    print("========== Calling LBLRTM ==========")
    # Change folder to where the LBLRTM executable is located
    with cd(lbl_location):
        # Run LBLRTM (the string should be the name of the LBLRTM executable)
        sub.call("lblrtm_v12.17_linux_intel_dbl")
        # Move all files somewhere to be saved
        # IF this step is skipped, LBLRTM will overwrite these
        # files when it is run again
        os.rename("TAPE5", save_location + "/TAPE5")
        os.rename("TAPE6", save_location + "/TAPE6")
        # os.rename("TAPE7", save_location + "/TAPE7")
        os.rename("TAPE11", save_location + "/TAPE11")
        os.rename("TAPE12", save_location + "/TAPE12")
        # Also move OD files if created
        if OD == 1:
            optical_files = glob.glob("OD*")
            for o_file in optical_files:
                os.rename(o_file, save_location + o_file)
    return


def load_tape12(save_location, mode):
    """Load the TAPE12 (that is in binary format) into a numpy array

    Args:
        save_location (path): path of TAPE12 specified in main script
        mode (int): see write_tape5.py: 0 - radiances only 1- radiances and transmittances
    Returns:
        tape12_array (array): first column is the wavenumber and second is radiances (optionally) transmittance is third

    Author: Sanjeevani Panditharatne (based on LW + SM script)
    """
    print("==== Loading TAPE12 as Numpy Array ====")
    panel_data = panpy.panel_file(save_location + "TAPE12", do_load_data=True)
    if mode == 1:
        rad_in_raw = panel_data.data1
        wn_in_raw = panel_data.v
        tape12_array = np.vstack([wn_in_raw, rad_in_raw])
    elif mode == 0:
        trans_in_raw = panel_data.data1
        rad_in_raw = panel_data.data1
        wn_in_raw = panel_data.v
        tape12_array = np.vstack([wn_in_raw, rad_in_raw, trans_in_raw])
    return tape12_array
