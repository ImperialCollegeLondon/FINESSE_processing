"""
Prepare interferograms for use in calibration
Produces interferograms averaged for each scan cycle
Only Averages hot and cold spectra
Skips any other angles

NEED TO: write function that algins, takes output centre bursts and algins ints
"""

from glob import glob
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import calibration_functions_sanjee as cal

# Location and names of files to combine
DATE = "20230220"
PATH = "/disk1/sm4219/WHAFFERS/"
INT_LOCATION = PATH + "/01_22_13_raw_finesse_test/"
# RUN NAME is the string at the end of the folder
RUN_NAME = "Measurement"
GUI_DATA_LOCATION = "/disk1/sm4219/WHAFFERS/01_22_13_raw_finesse_test/Vaisala_and_logs/20250122_logfile.txt"


# The AVERAGED_SAVE_LOCATION will be created if it does not already exist
AVERAGED_SAVE_LOCATION = PATH + f"/Processed_Data_test/{DATE}/prepared_ints_new/"
Path(AVERAGED_SAVE_LOCATION).mkdir(parents=True, exist_ok=True)
AVERAGING_LENGTH = 80

gui_data = cal.load_gui(GUI_DATA_LOCATION)

FOLDERS = glob(INT_LOCATION + "*" + RUN_NAME + "/")
FOLDERS.sort()
print(len(FOLDERS))

ints: list = []
times_all: list = []
n: list = []
centre_place = []

for FOLDER in FOLDERS:
    start_end_time = cal.find_time(FOLDER)
    times_all.append(start_end_time)

angles_all = []
for time in times_all:
    angle, angle_std = cal.colocate_time_range_gui(gui_data, time, "angle")
    angles_all.append(angle)
# print(angles_all)

times: list = []
angles = []

for FOLDER, angle in zip(FOLDERS, angles_all):
    print("angle", angle)
    if angle not in [270.0, 225.0]:
        continue
    # print(f"Processing {FOLDER} with angle {angle}")
    int_temp, start_end_temp, n_temp, centre_place_temp = (
        cal.average_ints_in_folder_new(
            FOLDER, len_int=(57090 - 178), return_n=True, centre_place=True
        )
    )
    ints.append(int_temp)
    times.append(start_end_temp)
    n.append(n_temp)
    centre_place.append(centre_place_temp)
    angles.append(angle)

# len_int=57090
# print(np.shape(centre_place), np.shape(angles))
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
    fig1, ax1 = plt.subplots(1, 1)
    ax1.plot(interferogram)
    ax1.set(
        title=f"Start time: {times[i][0]:.0f} Angle: {angles[i]}",
        ylim=(-0.15, 0.15),
        # xlim=(20000, 37000),
    )
    fig1.savefig(AVERAGED_SAVE_LOCATION + "int_%.0f.png" % times[i][0])
    plt.close(fig1)
