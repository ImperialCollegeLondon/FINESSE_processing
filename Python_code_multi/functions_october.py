from glob import glob
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import calibration_functions_sanjee as cal

#  NOTES TO SOPHIE:
# This function returns lots of texts files 

def prepare_ints(all_folders, gui_data, save_path, int_location):

    ints: list = []
    n: list = []
    centre_place: list = []

    for FOLDER in all_folders:
        # print("HERE is folder:", FOLDER)
        times: list = []
        # Path(INDIVIDUAL_SAVE_LOCATION + FOLDER[len(INT_LOCATION) :]).mkdir(
        #     parents=True, exist_ok=True
        # )

    int_temp, start_end_temp, n_temp, centre_place_temp = (
        cal.average_ints_in_folder_return_individuals(
            FOLDER, len_int=57090, return_n=True, centre_place=True
        )
    )
    ints = int_temp
    # times.append(start_end_temp)
    print("OFFSETTING TIME BY 5 SECONDS)")
    for t in start_end_temp:
        times.append(t - 5)
    n = n_temp
    centre_place = centre_place_temp
    angles = []

    for i, interferogram in enumerate(ints):
        cal.update_figure(1)
        run_track = run + 1

        gui_index_start = gui_data["time"].sub(times[i] - 1).abs().idxmin()
        gui_index_end = gui_data["time"].sub(times[i] + 1).abs().idxmin()
        variable = gui_data.loc[gui_index_start:gui_index_end, "angle"]
        angle, angle_std = np.mean(variable), np.std(variable)
        angles = angle

        header = (
            "Interferogram %i of %i\n" % (i + 1, len(ints))
            + "Start and end times (seconds since midnight)\n"
            + "%.1f " % (times[i])
            + "Mirror angle\n%.1f\n" % angles
        )
        print(header)
        np.savetxt(
            save_path
            + FOLDER[len(int_location) :]
            + "int_%.0f.txt" % times[i],
            interferogram,
            header=header,
        )
        return
    

