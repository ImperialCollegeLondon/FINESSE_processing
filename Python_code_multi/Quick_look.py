"""
Quick look at final data
"""

import numpy as np
import calibration_functions_sanjee as cal
import matplotlib.pyplot as plt

"""
# Name the file you want to look at
filename = "/disk1/sm4219/WHAFFERS/Processed_Data_test/20230220/calibrated_trial2/calibrated_spectrum_47945.0.txt"
filenames = "/disk1/sm4219/WHAFFERS/Processed_Data_test/20230220/calibrated_trial1calibrated_spectrum_(47192.0, 47251.0)_shift24.txt"

filelocation = "/disk1/sm4219/WHAFFERS/Processed_Data_test/20230220/calibrated_trial1/"
SAVE = "/disk1/sm4219/WHAFFERS//Processed_Data_test/20230220/calibrated_trial2/"


def load_data(filename):
    data = np.loadtxt(filename, skiprows=20)  # SKIP the header

    # Extract variables from each column
    wn = data[:, 0]
    radiance = data[:, 1]
    # nesr = data[:, 2]
    # pos_calib_error = data[:, 3]
    # neg_calib_error = data[:, 4]

    return wn, radiance


wn, radiance = load_data(filename)

print(wn[1:], radiance[1:])
# PLOTTING CODE
# Could add in blackbody curve here
# Could add in LBLRTM simulation spectra output
fig = plt.figure(figsize=(8, 6))
plt.plot(wn[1:], radiance[1:], label="FINESSE data")
plt.xlim(400, 1600)
plt.ylim(0, 0.12)
plt.ylabel("Radiance / [W m-2 sr-1 / cm-1]")
plt.xlabel("Wavenumbers / [cm-1]")
plt.legend()
plt.savefig(SAVE + "final_look_plot.png")
plt.close()

"""

# LOOKING AT THEM ALL

import os
import re
import numpy as np
import matplotlib.pyplot as plt

# File locations
filelocation = "/disk1/sm4219/WHAFFERS/Processed_Data_test/20230220/calibrated_trial3/"
SAVE = "/disk1/sm4219/WHAFFERS/Processed_Data_test/20230220/calibrated_trial3/"


# Function to load data
def load_data(filename):
    data = np.loadtxt(filename, skiprows=20)  # SKIP the header

    # Extract variables from each column
    wn = data[:, 0]
    radiance = data[:, 1]
    # pos_calib_error = data[:, 3]
    # neg_calib_error = data[:, 4]

    return wn, radiance


# Plot all files
fig, ax = plt.subplots(figsize=(8, 6))

# Regular expression pattern to extract numbers in the filename
pattern = re.compile(r"calibrated_spectrum_(\d+\.\d+)\.txt")

for filename in os.listdir(filelocation):
    match = pattern.match(filename)
    if match:
        # Extract the number from the filename
        label = match.group(1)  # This will give the number inside the filename
        filepath = os.path.join(filelocation, filename)
        wn, radiance = load_data(filepath)
        ax.plot(wn[1:], radiance[1:], label=label)

# Formatting the plot
ax.set_xlim(400, 1600)
ax.set_ylim(0, 0.12)
ax.set_xlabel("Wavenumbers / [cm⁻¹]")
ax.set_ylabel("Radiance / [W m⁻² sr⁻¹ cm⁻¹]")
ax.legend(title="Spectral Ranges", fontsize=8, loc="upper right")
plt.title("Calibrated Spectra")

# Save and close the plot
plt.savefig(os.path.join(SAVE, "final_look_plot.png"))
plt.close()

print("Plot saved successfully.")
