"""
Calculate spectra from interferograms averaged
in each cycle
"""

from glob import glob
from pathlib import Path
import numpy as np
import calibration_functions_sanjee as cal
from math import floor

DATE = "20230220"
PATH = "/disk1/sm4219/WHAFFERS/"
INT_LOCATION = PATH + "/01_22_13_raw_finesse_test/"
# RUN NAME is the string at the end of the folder
RUN_NAME = "Measurement"
GUI_DATA_LOCATION = "/disk1/sm4219/WHAFFERS/01_22_13_raw_finesse_test/Vaisala_and_logs/20250122_logfile.txt"

# The INDIVIDUAL_SAVE_LOCATION will be created if it does not already exist
INDIVIDUAL_SAVE_LOCATION = (
    PATH + f"/Processed_Data_test/prepared_individual_ints/"
)

SPECTRUM_LOCATION = DATA_LOCATION + "calibrated_spectra/"
AVERAGED_SAVE_LOCATION = PATH + f"/Processed_Data_test/{DATE}/prepared_ints_new/"
Path(SPECTRUM_LOCATION).mkdir(parents=True, exist_ok=True)
OPD = 1.21
OUTPUT_FREQUENCY = 0.0605 / OPD
CAL_OFFSET = 0.2  # K
STRETCH_FACTOR = 1.00016

gui_data = cal.load_gui(GUI_DATA_LOCATION)

# Find all averaged interferogram files
"Averaged only contains HBB + CBB"
int_list = glob(AVERAGED_INT_LOCATION + "*.txt")
int_list.sort()

"This will contain all"
FOLDERS = glob(INT_LOCATION + "*" + RUN_NAME + "/")
FOLDERS.sort()

for FOLDER in FOLDERS:
        int_2d = cal.chop_int(FOLDER, len_int=(57090-178), n_chop=4)

"""
PHASE SHIFT
  FOR sh=22,24 DO BEGIN
  dum(100L-sh:57000L-sh) = dum_hot(100L-sh:57000L-sh)-allints(view_180(view_count180),sp,100L:57000L)

QUALITY CHECK
Using a 0.01 threshold on the standard deviation in the 600 to 650 cm-1
If none of the three meet this criteria do not store the associated single spectra

      dum(0:250)=spe_phase(ind,cycle,sp,index(0):index(1))
      dum1=moment(dum)
      std(ind,cycle,sp)=sqrt(dum1(1))
"""

"Below works on certain script file as based on indexing"
# Load interferograms and get HBB and CBB temps
ints = []
HBB_temps = []
HBB_std = []
CBB_temps = []
CBB_std = []
angles = []
times = []
total_ints = len(int_list)
for i, name in enumerate(int_list):
    if i % 5 == 0:
        print("Loading %i of %i" % (i, total_ints))
    print(name)
    inter_temp, times_temp, angle_temp = cal.load_averaged_int(name)
    HBB_temp, HBB_std_temp = cal.colocate_time_range_gui(
        gui_data,
        times_temp,
        "HBB",
    )
    CBB_temp, CBB_std_temp = cal.colocate_time_range_gui(
        gui_data,
        times_temp,
        "CBB",
    )
    ints.append(inter_temp)
    times.append(times_temp)
    angles.append(angle_temp)
    HBB_temps.append(HBB_temp)
    HBB_std.append(HBB_std_temp)
    CBB_temps.append(CBB_temp)
    CBB_std.append(CBB_std_temp)

print("Interferograms loaded")
for i, angle in enumerate(angles):
    print(i, angle)

# THIS IS WHERE YOU REMOVE EXTRA INTERFEROGRAMS
# to_delete = [0, 201, 202, 203]
# to_delete = [0, 124]  # water 2
# to_delete = [0, 1, 2, 3, 4, 5, 6, 7, 20, 21, 64, 65]  # water 3
# to_delete = [0, 7, 8, 165, ]  # Water 4
# to_delete.sort(reverse=True)

print(angles)

# for index in to_delete:
#     ints.pop(index)
#     HBB_temps.pop(index)
#     HBB_std.pop(index)
#     CBB_temps.pop(index)
#     CBB_std.pop(index)
#     angles.pop(index)
#     times.pop(index)

# Check all ok
if all((x == 270.0 for x in angles[::4])):
    print("HBB angles ok")
else:
    print(angles[::4])
    print("HBB angles not in expected positions")
    exit()
if all((x == 225.0 for x in angles[1::4])):
    print("CBB angles ok")
else:
    print(angles[1::4])
    print("CBB angles not in expected positions")
    exit()

SCENE_NUMBER = floor(len(ints) / 3)
for i in range(SCENE_NUMBER):
    print("Spectrum %i of %i" % (i + 1, SCENE_NUMBER))
    # Customise for inputs
    HBB_index = i * 4
    CBB_index = i * 4 + 1
    scene_index = i * 4 + 2
    if not angles[HBB_index] == 270.0:
        print("HBB angles wrong")
        exit()
    if not angles[CBB_index] == 225.0:
        print("CBB angles wrong")
        exit()
    (
        wn,
        rad,
        NESR,
        (plus_cal_error, minus_cal_error),
    ) = cal.calibrate_spectrum_with_cal_error(
        ints[scene_index],
        ints[HBB_index],
        ints[CBB_index],
        HBB_temps[HBB_index],
        CBB_temps[CBB_index],
        np.sqrt(HBB_std[HBB_index] ** 2 + CAL_OFFSET**2),
        np.sqrt(CBB_std[CBB_index] ** 2 + CAL_OFFSET**2),
        fre_interval=OUTPUT_FREQUENCY,
    )
    # Stretch spectrum by pre calculated amount
    wn = wn * STRETCH_FACTOR
    header = (
        "Spectrum %i of %i including wn stretch\n\n" % (i + 1, SCENE_NUMBER)
        + "Scene\nStart and end times (seconds since midnight)\n"
        + "%.3f %.3f\n" % (times[scene_index][0], times[scene_index][1])
        + "Angle %.2f\n\n" % angles[scene_index]
        + "Hot black body\nStart and end times (seconds since midnight)\n"
        + "%.3f %.3f\n" % (times[HBB_index][0], times[HBB_index][1])
        + "Temperature (C)\n%.3f +/- %.3f\n\n"
        % (HBB_temps[HBB_index], HBB_std[HBB_index])
        + "Cold black body\nStart and end times (seconds since midnight)\n"
        + "%.3f %.3f\n" % (times[CBB_index][0], times[CBB_index][1])
        + "Temperature (C)\n%.3f +/- %.3f\n\n"
        % (CBB_temps[CBB_index], CBB_std[CBB_index])
        + "Wavenumber (cm-1), Radiance, NESR, "
        + "+ve Calibration error, -ve Calibration error"
    )
    print(header, "\n")
    data_out = np.column_stack((wn, rad, NESR, plus_cal_error, minus_cal_error))
    np.savetxt(
        SPECTRUM_LOCATION + "%i.txt" % int(times[scene_index][0]),
        data_out,
        header=header,
    )
