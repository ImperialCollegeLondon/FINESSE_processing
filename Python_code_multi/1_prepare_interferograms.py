"""
Prepare interferograms for use in calibration
Produces interferograms averaged for each scan cycle
"""

from glob import glob
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import calibration_functions_sanjee as cal

# Location and names of files to combine
DATE = "20230220"
PATH = '/disk1/Andoya/sp1016/'
INT_LOCATION = PATH+ f"Raw_Data/{DATE}/"
# RUN NAME is the string at the end of the folder
RUN_NAME = "zenith_test1"
GUI_DATA_LOCATION = INT_LOCATION + "clear_sky1-20230220103722.log"

PATH2 = '/disk1/sm4219/GIT/FINESSE_CAL/'

# The AVERAGED_SAVE_LOCATION will be created if it does not already exist
AVERAGED_SAVE_LOCATION = PATH2 + f"/Processed_Data_soph/{DATE}/prepared_ints/"
Path(AVERAGED_SAVE_LOCATION).mkdir(parents=True, exist_ok=True)
AVERAGING_LENGTH = 40

gui_data = cal.load_gui(GUI_DATA_LOCATION)

FOLDERS = glob(INT_LOCATION + "*" + RUN_NAME + "/")
FOLDERS.sort()
print(len(FOLDERS))

ints: list = []
times: list = []
n: list = []
centre_place: list = []

for FOLDER in FOLDERS:
    int_temp, start_end_temp, n_temp, centre_place_temp = cal.average_ints_in_folder(
        FOLDER,
        len_int=57090,
        return_n=True,
        centre_place=True
    )
    ints.append(int_temp)
    times.append(start_end_temp)
    n.append(n_temp)
    centre_place.append(centre_place_temp)

angles = []
for time in times:
    angle, angle_std = cal.colocate_time_range_gui(gui_data, time, "angle")
    angles.append(angle)
print(angles)

cal.update_figure(1)
for i, interferogram in enumerate(ints):
    header = (
        "Averaged interferogram %i of %i\n" % (i + 1, len(ints))
        + "Start and end times (seconds since midnight)\n"
        + "%.1f %.1f\n" % (times[i][0], times[i][1])
        + "Mirror angle\n%.1f\n" % angles[i]
    )
    print(header)
    np.savetxt(
        AVERAGED_SAVE_LOCATION + "int_%.0f.txt" % times[i][0],
        interferogram,
        header=header,
    )
    fig1, ax1 = plt.subplots(1,1)
    ax1.plot(interferogram)
    ax1.set(
        title=f"Start time: {times[i][0]:.0f} Angle: {angles[i]}",
        ylim=(-0.15, 0.15),
        xlim=(20000, 37000)
    )
    fig1.savefig(AVERAGED_SAVE_LOCATION + "int_%.0f.png" % times[i][0])
    plt.close(fig1)
