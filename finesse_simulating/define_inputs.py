from module_function_list import *

# Specify location of LBLRTM executable
lbl_location = "/net/thunder/data1/sp1016/lblrtm_12.17/"

# Specify location to save the output files
save_location = "/net/thunder/data1/sp1016/FINESSE_LBLRTM/finesse_processing/finesse_simulating/example_output/"

# Specify location of profiles
profile_folder = "example_input/"

# Specify atmospheric profile (note example profile has fummy z variable)
# See write_tape_5.py instructions for types of atmosphere and setting units
atmospheric_profile_name = profile_folder + "example_profile.txt"
pressure, z, temp, h2o, o3 = np.loadtxt(atmospheric_profile_name, unpack=True)

# Also set yaxis flag to note running in Pressure ('P') or Altitude ('A')
yaxis_flag = "P"

atm = 5  # Sets other gases to standard profiles

# Set flag if units not ppmv - must be included as input for write_tape5 function
h2o_flag = "H"
o3_flag = "C"

# Specify emissivity if desired
emissivity_profile_name = profile_folder + "need to complete"

# Specify view: angle = 0 for downwelling and =180 for upwelling
angle = 0
h_start = pressure[-1]  # Radiation calculation starts from altitude in hPa
h_obs = pressure[0]  ## Pressure height of observation (in this case the ground)

h_start_blackbody_surface = True  # Assuming black body at
h_start_temp = 2.7

# Set the wavenumber range and resolution
wn_range = [300, 1600]
res = 0.01

# Set the mode
mode = 1  # 1 = radiance, 0 = transmission
OD = 0  # 0 = no optical depth files

write_tape5(
    (z / 1000),
    pressure,
    temp,
    h2o,
    h_start_temp,
    h_obs,
    h_start,
    wn_range,
    angle,
    atm,
    mode,
    od=OD,
    t5=lbl_location + "/TAPE5",
    h2o_flag=h2o_flag,
    o3_flag=o3_flag,
    yaxis_flag=yaxis_flag,
    blackbody=h_start_blackbody_surface,
    res=res,
)
