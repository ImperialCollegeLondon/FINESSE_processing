
"""
Quick look at final data
"""
import numpy as np
import calibration_functions_sanjee as cal
import matplotlib.pyplot as plt

# Name the file you want to look at 
filename = "/disk1/sm4219/Testing_FINESSE_plots/Laura_response_part3/42017.txt"
SAVE = "/disk1/sm4219/Testing_FINESSE_plots/Laura_response_part3/"

def load_data(filename):
    """Loads data from the specified file and returns wavenumber and radiance."""
    data = np.loadtxt(filename, skiprows=20)  # SKIP the header
    
    # Extract variables from each column
    wn = data[:, 0]
    radiance = data[:, 1]
    nesr = data[:, 2]
    pos_calib_error = data[:, 3]
    neg_calib_error = data[:, 4]
    
    return wn, radiance, nesr, pos_calib_error, neg_calib_error

wn, radiance, nesr, pos_calib_error, neg_calib_error = load_data(filename)

# PLOTTING CODE
# Could add in blackbody curve here
# Could add in LBLRTM simulation spectra output
fig = plt.figure(figsize=(8, 6))
plt.plot(wn, radiance, label='FINESSE data')
plt.xlim(400,1600)
plt.ylim(0,0.12)
plt.ylabel("Radiance / [W m-2 sr-1 / cm-1]")
plt.xlabel("Wavenumbers / [cm-1]")
plt.legend()
plt.savefig(SAVE + "final_look_plot.png")

