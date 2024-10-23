# %%
"""
Calculate spectra from interferograms 
BUT single spectra
based on spectra_in_cycles
NOT WORKING 
NEEDS FIXING!
"""

from glob import glob
from pathlib import Path
import numpy as np
import calibration_functions_sanjee as cal
from math import floor
import glob

DATE = "20230220"
PATH = '/disk1/Andoya/sp1016/'
# DATA_LOCATION = PATH+f"Processed_Data_FOR_SOPHIE/{DATE}/"

PATH2 = '/disk1/sm4219/GIT/FINESSE_CAL/'
DATA_LOCATION = PATH2+f"/Processed_Data_soph/{DATE}/"
AVERAGED_INT_LOCATION = DATA_LOCATION + "prepared_ints/"
SPECTRUM_LOCATION = DATA_LOCATION + "calibrated_spectra/"
GUI_DATA_LOCATION = PATH +f"Raw_Data/{DATE}/"+ "clear_sky1-20230220103722.log"

PATH3 = '/disk1/sm4219/GIT/'
# The INDIVIDUAL_SAVE_LOCATION will be created if it does not already exist
INDIVIDUAL_SAVE_LOCATION = PATH3+f"Processed_Data_soph_single/prepared_individual_ints/"
Path(INDIVIDUAL_SAVE_LOCATION).mkdir(parents=True, exist_ok=True)
INDIVIDUAL_SPECTRUM_SAVE_LOCATION = PATH3+ f"PROCESSED_EXAMPLE/Processed_Data/individual_spectra/"

Path(SPECTRUM_LOCATION).mkdir(parents=True, exist_ok=True)
OPD = 1.21
OUTPUT_FREQUENCY = 0.0605 / OPD
CAL_OFFSET = 0.2  # K
STRETCH_FACTOR = 1.00016

gui_data = cal.load_gui(GUI_DATA_LOCATION)

"AVERAGED HERE"
# Find all averaged interferogram files
int_list_avg = glob.glob(AVERAGED_INT_LOCATION + "*.txt")
int_list_avg.sort()
total_ints = len(int_list_avg)
angles = []
ints = []
times = []

"AVERAGED TRYING TO GET ALL ANGLES AND INTS AND TIMES"
for i, name in enumerate(int_list_avg[:total_ints]):
    inter_temp, times_temp, angle_temp = cal.load_averaged_int(name)
    angles.append(angle_temp)
    ints.append(inter_temp)
    times.append(times_temp)

"FIND INDICIES OF CAL VIEWS WITHIN AVERAGED"
cal_sequence = [270, 225]
cal_locations = [i for i in range(len(angles))
    if angles[i:i+len(cal_sequence)] == cal_sequence]

RESP_NUMBER = len(cal_locations)
print("Number of response functions: ", RESP_NUMBER)

"SAVING PROPERTIES OF HBB AND CBB FOR AVERAGED"
cal.update_figure(1, size=(15, 15/1.68))
for i, index in enumerate(cal_locations):
    print("Response %i of %i" % (i + 1, RESP_NUMBER))
    int_HBB = ints[index]
    int_CBB = ints[index+1]
    # HBB = HBB_temps[index]
    # CBB = CBB_temps[index+1]
    # HBB_error = HBB_std[index]
    # CBB_error = CBB_std[index + 1]
    HBB_angle = angles[index]
    CBB_angle = angles[index + 1]
    HBB_times = times[index]
    CBB_times = times[index + 1]



""" 
hbb_int, hbb_time, hbb_angle = cal.load_averaged_int(HBB_PATH)
cbb_int, cbb_time, cbb_angle = cal.load_averaged_int(CBB_PATH)
"""
"SINGLE HERE"
RUN_NAME = "zenith_test1"
single_INT_LOCATION = "/disk1/sm4219/GIT/FINESSE_CAL/Processed_Data_soph_single/prepared_individual_ints/"
FOLDERS = glob.glob(single_INT_LOCATION + "*" + RUN_NAME + "/")
FOLDERS.sort()
print("Folders", FOLDERS)

FOLDERS_EXAMINING=FOLDERS[0:1]

int_list = []
for folder in FOLDERS_EXAMINING:
    int_files = glob.glob(folder + "*.txt")
    int_list.extend(int_files)

int_list.sort()
print("INT files:", int_list)
total_ints = len(int_list)

# Load interferograms and get HBB and CBB temps
ints = []
HBB_temps = []
HBB_std = []
CBB_temps = []
CBB_std = []
angles = []
times = []
wn_calibrateds = []
rad_calibrateds = []
nesr_calibrateds = []
cal_errors = []
total_ints = len(int_list)

for FOLDER in FOLDERS_EXAMINING:  # folders 2, 3 are 50º; folders 4, 5 are 130º; change numbers to whatever folder is desired
    print("processing folder " + str(FOLDER))
    # Find all interferogram files
    int_list = glob.glob(FOLDER + "*.txt")
    int_list.sort()
    total_ints = len(int_list)

    # Load interferograms and get HBB and CBB temps

    # get HBB and CBB average interferograms (used for calibration)
    hbb_int, hbb_time, hbb_angle = int_HBB, HBB_times, HBB_angle
    cbb_int, cbb_time, cbb_angle =  int_CBB, CBB_times, CBB_angle

    for i, name in enumerate(int_list):
        # as in 3a_calibrate_spectra_in_cycles, get interferogram data
        if i % 5 == 0:
            print("Loading %i of %i" % (i, total_ints))
        inter_temp, times_temp, angle_temp = cal.load_single_int(
            name)  # using the function for averaged interferograms, but passing a single (not averaged) interferogram into it
       
        HBB_temp, HBB_std_temp = cal.colocate_time_range_gui(
            gui_data, times_temp, "HBB", )
        CBB_temp, CBB_std_temp = cal.colocate_time_range_gui(
            gui_data, times_temp, "CBB", )
        ints.append(inter_temp)
        times.append(times_temp)
        angles.append(angle_temp)
        HBB_temps.append(HBB_temp)
        HBB_std.append(HBB_std_temp)
        CBB_temps.append(CBB_temp)
        CBB_std.append(CBB_std_temp)

        # get spectrum and add to lists (technically not all the lists are not used, but are here for completion)
        wn_calibrated, rad_calibrated, nesr_calibrated, (
            plus_cal_error, minus_cal_error) = cal.calibrate_spectrum_with_cal_error(
            inter_temp, hbb_int, cbb_int, HBB_temp, CBB_temp, HBB_std_temp, CBB_std_temp, fre_interval=OUTPUT_FREQUENCY)
        wn_calibrated *= STRETCH_FACTOR  # apply pre-determined stretch factor
        wn_calibrateds.append(wn_calibrated)
        rad_calibrateds.append(rad_calibrated)
        nesr_calibrateds.append(nesr_calibrated)
        cal_errors.append((plus_cal_error, minus_cal_error))
        print(angle_temp)



for FOLDER in FOLDERS_EXAMINING:  # folders 2, 3 are 50º; folders 4, 5 are 130º; change numbers to whatever folder is desired
    print("processing folder " + str(FOLDER))
    int_list = glob(FOLDER + "*.txt")
    int_list.sort()
    total_ints = len(int_list)
    Path(INDIVIDUAL_SPECTRUM_SAVE_LOCATION+FOLDER[len(INT_LOCATION):]).mkdir(parents=True, exist_ok=True)

    for i, name in enumerate(int_list):
        wn_calibrated = wn_calibrateds[i]
        rad_calibrated = rad_calibrateds[i]
        nesr_calibrated = nesr_calibrateds
        (plus_cal_error, minus_cal_error) = cal_errors[i]
        # output data (same way as in 3a_calibrate_spectra_in_cycles)
        data_out = np.column_stack(
            (wn_calibrated, rad_calibrated, nesr_calibrated, plus_cal_error, minus_cal_error))

        SCENE_NUMBER = i  # not sure about these, so just leaving them as the counter
        scene_index = i

        header = (
                "Spectrum %i of %i including wn stretch\n\n" % (i + 1, SCENE_NUMBER)
                + "Scene\nStart and end times (seconds since midnight)\n"
                + "%.3f %.3f\n" % (times[scene_index][0], times[scene_index][1])
                + "Angle %.2f\n\n" % angles[scene_index]
                + "Hot black body\nStart and end times (seconds since midnight)\n"
                + "%.3f %.3f\n" % (hbb_time[0], hbb_time[1])
                + "Temperature (C)\n%.3f +/- %.3f\n\n"
                % (HBB_temps[i], HBB_std[i])
                + "Cold black body\nStart and end times (seconds since midnight)\n"
                + "%.3f %.3f\n" % (cbb_time[0], cbb_time[1])
                + "Temperature (C)\n%.3f +/- %.3f\n\n"
                % (CBB_temps[i], CBB_std[i])
                + "Wavenumber (cm-1), Radiance, NESR, "
                + "+ve Calibration error, -ve Calibration error"
        )

        np.savetxt(
            INDIVIDUAL_SPECTRUM_SAVE_LOCATION +FOLDER[len(INT_LOCATION):] + "%i.txt" % int(times[scene_index][0]),
            data_out,
            header=header,
        )

        fig, axs1 = plt.subplots(nrows=2)
        fig.tight_layout()
        axs=axs1[0]
        axs.plot(wn_calibrated, rad_calibrated)
        axs.set_ylim(0, 0.2)
        axs.set_xlim(400, 1600)
        axs.set_xlabel('WN (cm$^{-1}$)')
        axs.set_ylabel('Radiance \n (W/m$^2$/sr/cm$^{-1}$)')

        axs=axs1[1]
        axs.plot(wn_calibrated, nesr_calibrated,label='NESR')
        axs.plot(wn_calibrated, plus_cal_error,label='+CAL')
        axs.set_ylim(0, 0.2)
        axs.set_xlim(400, 1600)
        axs.set_xlabel('WN (cm$^{-1}$)')
        axs.set_ylabel('Error \n (W/m$^2$/sr/cm$^{-1}$)')
        axs.legend()
        fig.suptitle('Angle ' + str(angles[scene_index]))
        fig.savefig(INDIVIDUAL_SPECTRUM_SAVE_LOCATION + FOLDER[len(INT_LOCATION):]+ "%i.jpg" % int(times[scene_index][0]), bbox_inches='tight')
        plt.close(fig)


"""




for i, name in enumerate(int_list):
    if i % 5 == 0:
        print("Loading %i of %i" % (i, total_ints))
    print(name)
    # inter_temp, times_temp, angle_temp = cal.load_averaged_int(name)

    inter_temp, times_temp, angle_temp = cal.load_single_int(name)  # using the function for averaged interferograms, but passing a single (not averaged) interferogram into it
       

    HBB_temp, HBB_std_temp = cal.colocate_time_range_gui(
        gui_data, times_temp, "HBB",)
    CBB_temp, CBB_std_temp = cal.colocate_time_range_gui(
        gui_data, times_temp, "CBB",)
    ints.append(inter_temp)
    times.append(times_temp)
    angles.append(angle_temp)
    HBB_temps.append(HBB_temp)
    HBB_std.append(HBB_std_temp)
    CBB_temps.append(CBB_temp)
    CBB_std.append(CBB_std_temp)




    # get spectrum and add to lists (technically not all the lists are not used, but are here for completion)
    wn_calibrated, rad_calibrated, nesr_calibrated, (
        plus_cal_error, minus_cal_error) = cal.calibrate_spectrum_with_cal_error(
        inter_temp, hbb_int, cbb_int, HBB_temp, CBB_temp, HBB_std_temp, CBB_std_temp, fre_interval=OUTPUT_FREQUENCY)
    wn_calibrated *= STRETCH_FACTOR  # apply pre-determined stretch factor
    wn_calibrateds.append(wn_calibrated)
    rad_calibrateds.append(rad_calibrated)
    nesr_calibrateds.append(nesr_calibrated)
    cal_errors.append((plus_cal_error, minus_cal_error))
    print(angle_temp)


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









# BELOW CODE IS FROM MULTI 

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
        np.sqrt(HBB_std[HBB_index]**2 + CAL_OFFSET**2),
        np.sqrt(CBB_std[CBB_index]**2 + CAL_OFFSET**2),
        fre_interval=OUTPUT_FREQUENCY,
    )
    # Stretch spectrum by pre calculated amount
    wn = wn*STRETCH_FACTOR
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
    data_out = np.column_stack(
        (wn, rad, NESR, plus_cal_error, minus_cal_error))
    np.savetxt(
        SPECTRUM_LOCATION + "%i.txt" % int(times[scene_index][0]),
        data_out,
        header=header,
    )
"""
# %%

# %%
