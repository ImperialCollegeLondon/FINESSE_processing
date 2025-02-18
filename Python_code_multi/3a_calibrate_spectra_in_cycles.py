"""
Calculate spectra from interferograms averaged
in each cycle
"""

from glob import glob
from pathlib import Path
import numpy as np
import calibration_functions_sanjee as cal
from math import floor
import matplotlib.pyplot as plt

DATE = "20230220"
PATH = "/disk1/sm4219/WHAFFERS/"
INT_LOCATION = PATH + "/01_22_13_raw_finesse_test/"
# RUN NAME is the string at the end of the folder
RUN_NAME = "Measurement"
GUI_DATA_LOCATION = "/disk1/sm4219/WHAFFERS/01_22_13_raw_finesse_test/Vaisala_and_logs/20250122_logfile.txt"

# The INDIVIDUAL_SAVE_LOCATION will be created if it does not already exist
INDIVIDUAL_SAVE_LOCATION = PATH + f"/Processed_Data_test/prepared_individual_ints/"
DATA_LOCATION = PATH + f"/Processed_Data_test/{DATE}/"
AVERAGED_INT_LOCATION = DATA_LOCATION + "prepared_ints_new/"
SPECTRUM_LOCATION = DATA_LOCATION + "calibrated_spectra/"
AVERAGED_SAVE_LOCATION = PATH + f"/Processed_Data_test/{DATE}/prepared_ints_new/"
Path(SPECTRUM_LOCATION).mkdir(parents=True, exist_ok=True)

FINAL_CAL_SAVED = PATH + f"/Processed_Data_test/{DATE}/calibrated_trial3/"
Path(FINAL_CAL_SAVED).mkdir(parents=True, exist_ok=True)

OPD = 1.21
OUTPUT_FREQUENCY = 0.0605 / OPD
CAL_OFFSET = 0.2  # K
STRETCH_FACTOR = 1.00016

gui_data = cal.load_gui(GUI_DATA_LOCATION)

# Find all averaged interferogram files
"Averaged only contains HBB + CBB"
int_list_avg = glob(AVERAGED_INT_LOCATION + "*.txt")
int_list_avg.sort()

# Load HBB and CBB interferograms and get HBB and CBB temps
cal_ints = []
HBB_temps = []
HBB_std = []
CBB_temps = []
CBB_std = []
cal_angles = []
cal_times = []
total_ints = len(int_list_avg)
for i, name in enumerate(int_list_avg):
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
    cal_ints.append(inter_temp)
    cal_times.append(times_temp)
    cal_angles.append(angle_temp)
    HBB_temps.append(HBB_temp)
    HBB_std.append(HBB_std_temp)
    CBB_temps.append(CBB_temp)
    CBB_std.append(CBB_std_temp)

print("cal_hbb", HBB_temps, CBB_temps)
# print("cal_times", cal_times)


"This will contain all"
FOLDERS = glob(INT_LOCATION + "*" + RUN_NAME + "/")
FOLDERS.sort()

times_all = []
for FOLDER in FOLDERS:
    # int_2d = cal.chop_int(FOLDER, len_int=(57090-178), n_chop=4)
    start_end_time = cal.find_time(FOLDER)
    times_all.append(start_end_time)

# FOR ANGLES IF WE WANT IT
times_180 = []
angles_all = []
for time in times_all:
    angle, angle_std = cal.colocate_time_range_gui(gui_data, time, "angle")
    angles_all.append(angle)

print(angles_all)

# Find 180 folder with nears 270 225 folders
for FOLDER, angle in zip(FOLDERS, angles_all):
    if angle not in [180.0]:
        continue
    start_end_time = cal.find_time(FOLDER)
    times_180.append(start_end_time)

print("Times 180", times_180)

for FOLDER, angle in zip(FOLDERS, angles_all):
    """
    1. This goes through folders and finds 180 folder views
    2. Finds nearest HBB and CBB view to that 180
    (Need to implement that takes before and after and averages)
    3. Goes into 180 folder and chops into 4 inteferograms
    """
    start_end_time = cal.find_time(FOLDER)  # Get the time for this FOLDER
    print(start_end_time[0], "time")
    # Find all indices of angle = 180.0
    if 180.0 in angles_all:
        # Loop of angles 180
        idx_180 = angles_all.index(180.0)  # First occurrence of 180.0

        # Find all index with angles of 270.0 and 225.0
        idx_270s = [i for i, a in enumerate(angles_all) if a == 270.0]
        idx_225s = [i for i, a in enumerate(angles_all) if a == 225.0]

        # Find nearest 270.0 and 225.0 (before or after)
        # Lambda is an anymous function that is taking absolute distance
        idx_270 = min(idx_270s, key=lambda i: abs(i - idx_180), default=None)
        idx_225 = min(idx_225s, key=lambda i: abs(i - idx_180), default=None)

        if idx_270 is not None and idx_225 is not None:
            # Get times for 270 and 225 angles
            time_270 = cal.find_time(FOLDERS[idx_270])
            time_225 = cal.find_time(FOLDERS[idx_225])

            # Find the index of these times in cal_times which contains the AVERAGED ints
            idx_time_270 = next(
                (i for i, t in enumerate(cal_times) if time_270 in t), None
            )
            idx_time_225 = next(
                (i for i, t in enumerate(cal_times) if time_225 in t), None
            )

            if idx_time_270 is not None and idx_time_225 is not None:
                # Extract HBB_temp and CBB_temp
                HBB_temp_nearest = HBB_temps[idx_time_270]
                CBB_temp_nearest = CBB_temps[idx_time_225]
                HBB_int_nearest = cal_ints[idx_time_270]
                CBB_int_nearest = cal_ints[idx_time_225]

                # **Skip folders where angle is NOT 180**
                if angle != 180.0:
                    continue  # Skip this folder and move to the next

                ints_names = glob(FOLDER + "/*.0")
                ints_names.sort()
                centre_places = []
                # Need to chop int files into four
                # ONLY GOING TO FIRST FILE IN INT NAMES
                for name in [ints_names[0]]:
                    print("Int name here:", name)
                    chopped_data = cal.chop_int(name, len_int=(57090 - 178), n_chop=4)
                    # print("Chopped data", chopped_data, np.shape(chopped_data))
                    # Isolating each of the columns
                    for col_idx in range(chopped_data.shape[0]):  # Number of columns
                        col_int = chopped_data[col_idx, :]  # Extract column values

                        # "IMPLEMENTING THE SHIFT"
                        # for shift in range(-1, 2):
                        # print("SCENE int nearest full and size 2", col_int, len(col_int))
                        hbb_int_crop = HBB_int_nearest[100:-100]
                        cbb_int_crop = CBB_int_nearest[100:-100]
                        # shift_int_scene =  col_int[100 + shift : - (100 - shift)]
                        shift_int_scene = col_int[100:-100]
                        # print("HBB and SCENE", hbb_int_crop, len(hbb_int_crop), shift_int_scene, len(shift_int_scene))
                        # raise(KeyboardInterrupt)
                        # Calibrate the spectrum using the shifted data
                        print("BB TEMPERATURE", HBB_temp_nearest, CBB_temp_nearest)
                        # plt.figure()
                        # plt.plot(shift_int_scene, label='scene')
                        # plt.plot(hbb_int_crop, label='hbb')
                        # plt.plot(cbb_int_crop, label='cbb')
                        # plt.title(shift)
                        # plt.legend()

                        (wn, rad, rad_complex, NESR) = (
                            cal.calibrate_spectrum_with_complex(
                                shift_int_scene,
                                hbb_int_crop,
                                cbb_int_crop,
                                HBB_temp_nearest,
                                CBB_temp_nearest,
                            )
                        )

                        # Create the header with the shift number and other relevant info
                        header = f"no shift, Folder: {FOLDER}, Time: {start_end_time}, HBB_temp: {HBB_temp_nearest}, CBB_temp: {CBB_temp_nearest}"
                        # NOTE NESR IS COMING OUT AS NANS
                        data_out = np.column_stack((wn, rad))
                        # Save the calibrated spectrum, include the time and shift number in the filename
                        save_filename = (
                            FINAL_CAL_SAVED
                            + f"calibrated_spectrum_{start_end_time[0]}.txt"
                        )
                        print(data_out.dtype)
                        np.savetxt(save_filename, data_out, header=header)
                        print("Saved to", save_filename)
                        # plt.figure()
                        # plt.plot(wn, rad)
                        # plt.plot(wn, rad_complex)
                        # plt.title(shift)
                        # plt.xlim(400,1600)
                        # plt.ylim(0,0.14)
                        # plt.show()

                        # else:
                        #     print("No valid shift found with QA below threshold.", name, col_idx)


"""
Code for shift...
    4. Shifts the 180 view with respect to HBB and CBB
    5. Calibrates returns complex rad
    6. Checks which shift gives minimum STD of complex rad in 600 to 650 region 
    7. Saves wn and real rad of minimum shift if std < 0.01

                        # Setting values for shifted spec
                        best_QA = float('inf')  
                        best_shift = None  
                        best_rad_complex = None
                        best_wn = None
                        best_rad = None
                        best_NESR = None
    
                        # "IMPLEMENTING THE SHIFT"
                        # for shift in range(-1, 2):
                        # print("SCENE int nearest full and size 2", col_int, len(col_int))
                        hbb_int_crop = HBB_int_nearest[100:-100]
                        cbb_int_crop = CBB_int_nearest[100:-100]
                        shift_int_scene =  col_int[100 + shift : - (100 - shift)]

                                                # Selecting region 600 to 650
                        crop_indexes = np.where((wn >= 600) & (wn <= 650))[0]
                        wn_cropped = wn[crop_indexes]
                        rad_complex_cropped = rad_complex[crop_indexes]
                        # print(wn_cropped)
                    
                        QA_check = np.std(rad_complex_cropped)
                        # CHOOSE the minimum QA
                            if QA_check < best_QA:  
                                best_QA = QA_check
                                best_shift = shift
                                best_rad_complex = rad_complex
                                best_wn = wn
                                best_rad = rad
                                best_NESR = NESR
                    
                        if best_QA < 0.01 and best_shift is not None:
"""
