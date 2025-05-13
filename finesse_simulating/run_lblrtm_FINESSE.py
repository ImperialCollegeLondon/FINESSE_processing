"""Run LBLRTM

Turned previous script into modular pieces of code

Authour: Sanjeevani Panditharatne
Written: 30/04/2025
"""

import sys

sys.path.insert(1, "src")
from module_function_list import *

# Inputs are specified in define_inputs.py which calls the write_tape5.py script

# Call LBLRTM to run simulation
call_lblrtm(lbl_location, save_location, OD)

# # Converts the TAPE12 output from a binary file into a numpy array.
tape12_array = load_tape12(save_location, mode)
high_res_wn = tape12_array[0, :]
high_res_spec = tape12_array[1, :]

# # Apply FINESSE OPD = 1.21 onto a sampling grid of 0.2 cm-1
wn_out, rad_out = process_spectrum_general(
    high_res_wn, high_res_spec, 0.2, 350, 1600, 1.21
)

# # Apply the FINESSE instrument line shape
ILS_LOCATION = "EM27_ILS_test1_3_25.sav"
ils = readsav(ILS_LOCATION)
ILS = ils["em27_ils"][:]
apodised_wn, apodised_spectrum = apply_ILS_sav(ILS, wn_out, rad_out, pad_length=10)

print("========== Finishing and Plotting ==========")

# Converted to mW
apodised_spectrum_mW = apodised_spectrum * 1e6

plt.plot(apodised_wn, apodised_spectrum_mW)
plt.xlabel("Wavenumber (cm$^{-1}$)")
plt.ylabel("Radiance (mW m$^{-2}$ sr$^{-1}$ cm)")
plt.savefig(save_location+"Output_Plot.jpg", dpi=300)

print("========== END ==========")
