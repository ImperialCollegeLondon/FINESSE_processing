"""
Calculate the response function for a set of
averaged interferograms.
n.b. at the moment this assumes an OPD of 1.8cm
and a boxcar apodisation function

THIS CODE is for the multi case and is working
There is a check on if the centrebursts are in the same place or not, will print statemnet if not

"""

from glob import glob
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import calibration_functions_sanjee as cal
from math import floor

DATE = "20230220"
PATH = "/disk1/sm4219/WHAFFERS/"
INT_LOCATION = PATH + "/01_22_13_raw_finesse_test/"
# RUN NAME is the string at the end of the folder
RUN_NAME = "Measurement"
GUI_DATA_LOCATION = "/disk1/sm4219/WHAFFERS/01_22_13_raw_finesse_test/Vaisala_and_logs/20250122_logfile.txt"

DATA_LOCATION = PATH + f"/Processed_Data_test/{DATE}/"
# DATA_LOCATION = PATH+f"Processed_Data_FOR_SOPHIE/{DATE}/"
AVERAGED_INT_LOCATION = DATA_LOCATION + "prepared_ints_new/"

RESPONSE_FUNCTION_LOCATION = DATA_LOCATION + "response_functions/"
Path(RESPONSE_FUNCTION_LOCATION).mkdir(parents=True, exist_ok=True)

gui_data = cal.load_gui(GUI_DATA_LOCATION)

# Find all averaged interferogram files
int_list = glob(AVERAGED_INT_LOCATION + "*.txt")
int_list.sort()


# Load interferograms and get HBB and CBB temps
ints = []
HBB_temps = []
HBB_std = []
CBB_temps = []
CBB_std = []
angles = []
times = []
total_ints = len(int_list)
# total_ints = 75
for i, name in enumerate(int_list[:total_ints]):
    if i % 25 == 0:
        print("Loading %i of %i" % (i, total_ints))
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
# FIND INDICIES OF CAL VIEWS
cal_sequence = [270, 225]
cal_locations = [
    i for i in range(len(angles)) if angles[i : i + len(cal_sequence)] == cal_sequence
]

print(angles, len(angles))

RESP_NUMBER = len(cal_locations)
print("Number of response functions: ", RESP_NUMBER)

cal.update_figure(1, size=(15, 15 / 1.68))
for i, index in enumerate(cal_locations):
    print("Response %i of %i" % (i + 1, RESP_NUMBER))
    int_HBB = ints[index]
    int_CBB = ints[index + 1]
    HBB = HBB_temps[index]
    CBB = CBB_temps[index + 1]
    HBB_error = HBB_std[index]
    CBB_error = CBB_std[index + 1]
    HBB_angle = angles[index]
    CBB_angle = angles[index + 1]
    HBB_times = times[index]
    CBB_times = times[index + 1]
    print("HBB_angle: ", HBB_angle)
    print("HBB temp: ", HBB)
    print("CBB_angle: ", CBB_angle)
    print("CBB temp: ", CBB, "\n")
    wn, resp_temp, resp_temp_unapp = cal.calculate_response_function(
        int_HBB,
        int_CBB,
        HBB,
        CBB,
    )
    header = (
        "Response function %i of %i\n\n" % (i + 1, RESP_NUMBER)
        + "Hot black body\nStart and end times (seconds since midnight)\n"
        + "%.3f %.3f\n" % (HBB_times[0], HBB_times[1])
        + "Temperature (C)\n%.3f +/- %.3f\n\n" % (HBB, HBB_error)
        + "Cold black body\nStart and end times (seconds since midnight)\n"
        + "%.3f %.3f\n" % (CBB_times[0], CBB_times[1])
        + "Temperature (C)\n%.3f +/- %.3f\n\n" % (CBB, CBB_error)
        + "Wavenumber (cm-1), "
        + "Response function\n"
    )
    print(header)
    data = np.column_stack((wn, resp_temp_unapp))

    centre_HBB = np.argmax(int_HBB)
    centre_CBB = np.argmax(int_HBB)
    if centre_HBB - centre_CBB != 0:
        print("Difference between HBB and CBB centrebursts")

    np.savetxt(
        RESPONSE_FUNCTION_LOCATION + "%i.txt" % HBB_times[0], data, header=header
    )
    fig1, ax1 = plt.subplots(1, 1)
    ax1.plot(wn, resp_temp_unapp, lw=0.7)
    ax1.set(
        title=f"Start time: {HBB_times[0]:.0f}",
        ylim=(0, 12),
        xlim=(350, 2500),
        ylabel="Response function",
        xlabel=r"Wavenumbers (cm$^{-1}$)",
    )
    fig1.savefig(RESPONSE_FUNCTION_LOCATION + "%i.png" % HBB_times[0])
    plt.close(fig1)
