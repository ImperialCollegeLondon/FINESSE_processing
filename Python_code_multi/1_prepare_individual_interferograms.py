"""
Prepare interferograms for use in calibration
Produces interferograms averaged for each scan cycle

THIS CODE IS WORKING
"""

from glob import glob
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import calibration_functions_sanjee as cal

DATE = "20230220"
PATH = '/disk1/Andoya/sp1016/'
INT_LOCATION = PATH+ f"Raw_Data/{DATE}/"
# RUN NAME is the string at the end of the folder
RUN_NAME = "zenith_test1"
GUI_DATA_LOCATION = INT_LOCATION + "clear_sky1-20230220103722.log"

PATH2 = '/disk1/sm4219/GIT/FINESSE_CAL/'
# The INDIVIDUAL_SAVE_LOCATION will be created if it does not already exist
INDIVIDUAL_SAVE_LOCATION = PATH2+f"Processed_Data_soph_single/prepared_individual_ints/"
Path(INDIVIDUAL_SAVE_LOCATION).mkdir(parents=True, exist_ok=True)
SAVE_LOACTION = PATH2+f"Processed_Data_soph_single/"
gui_data = cal.load_gui(GUI_DATA_LOCATION)

FOLDERS = glob(INT_LOCATION + "*" + RUN_NAME + "/")
FOLDERS.sort()

ints: list = []
n: list = []
centre_place: list = []
run = 0 

for FOLDER in FOLDERS:
    print("HERE is folder:", FOLDER)
    times: list = []
    Path(INDIVIDUAL_SAVE_LOCATION+FOLDER[len(INT_LOCATION):]).mkdir(parents=True, exist_ok=True)

    int_temp, start_end_temp, n_temp, centre_place_temp = cal.average_ints_in_folder_return_individuals(
        FOLDER,
        len_int=57090,
        return_n=True,
        centre_place=True
    )
    ints=int_temp
    # times.append(start_end_temp)
    print('OFFSETTING TIME BY 5 SECONDS)')
    for t in start_end_temp:
        times.append(t-5)
    n=n_temp
    centre_place=centre_place_temp
    angles = []

    for i, interferogram in enumerate(ints):
        cal.update_figure(1)
        run_track = run + 1

        gui_index_start = gui_data["time"].sub(times[i]-1).abs().idxmin()
        gui_index_end = gui_data["time"].sub(times[i]+1).abs().idxmin()
        variable = gui_data.loc[gui_index_start:gui_index_end, 'angle']
        angle, angle_std= np.mean(variable), np.std(variable)
        angles=angle

        header = (
            "Interferogram %i of %i\n" % (i + 1, len(ints))
            + "Start and end times (seconds since midnight)\n"
            + "%.1f " % (times[i])
            + "Mirror angle\n%.1f\n" % angles
        )
        print(header)
        np.savetxt(
            INDIVIDUAL_SAVE_LOCATION +FOLDER[len(INT_LOCATION):]+ "int_%.0f.txt" % times[i],
            interferogram,
            header=header,
        )
        fig1, ax1 = plt.subplots(1,1)
        ax1.plot(interferogram)
        ax1.set(
            title=f"Start time: {times[i]:.0f} Angle: {angles}",
            ylim=(-0.15, 0.15),
            xlim=(20000, 37000)
        )
        fig1.savefig(INDIVIDUAL_SAVE_LOCATION +FOLDER[len(INT_LOCATION):]+ "int_%.0f.png" % times[i])
        plt.close(fig1)
        print("Figure saved to:", INDIVIDUAL_SAVE_LOCATION +FOLDER[len(INT_LOCATION):]+ "int_%.0f.png" % times[i])
        print("END OF RUN NUMBER", run_track)
        # raise(KeyboardInterrupt)
