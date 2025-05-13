from module_function_list import *

# Specify location of LBLRTM executable
lbl_location = "/net/thunder/data1/sp1016/lblrtm_12.17/"

# Specify location to save the output files
save_location = "/net/thunder/data1/sp1016/FINESSE_LBLRTM/"
# Specify location of profiles
profile_folder = "/net/sirocco/disk1/Andoya/sp1016/LBLRTM_SIMULATIONS/ERA5_DATA/"

# Specify atmospheric profile
# See write_tape_5.py instructions for types of atmosphere and setting units
atmospheric_profile_name  = profile_folder + "era5_20230221_1600_2100.nc"
atmos_nc = xr.open_dataset(atmospheric_profile_name)
atmos_nc=atmos_nc.sel(time=atmos_nc.time.values[1],latitude = atmos_nc.latitude.values[0], longitude=atmos_nc.longitude.values[0])

pressure = np.flip(atmos_nc.level.values)
temp = np.flip(atmos_nc.t.values)
h2o = np.flip(atmos_nc.r.values)
o3 =np.flip( atmos_nc.o3.values )* 1E3

# Load dummy z because running in pressure
z = np.full_like(pressure,0)

atm = 5  # Sets other gases to standard profiles

# Set flag if units not ppmv - must be included as input for write_tape5 function
h2o_flag='H'
o3_flag='C'

# Specify emissivity if desired
emissivity_profile_name = profile_folder + 'need to complete'

# Specify view: angle = 0 for downwelling and =180 for upwelling
angle=0
h_start =  pressure[-1] # Radiation calculation starts from altitude in hPa
h_obs = pressure[0] ## Pressure height of observation (in this case the ground)

h_start_blackbody_surface = True  # Assuming black body at
h_start_temp =2.7

# Set the wavenumber range and resolution
wn_range = [300,1600]
res=0.01

# Set the mode
mode = 1  # 1 = radiance, 0 = transmission
OD = 0  # 0 = no optical depth files

write_tape5(
    (z/1000),
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
    t5= lbl_location+"/TAPE5",
    h2o_flag = h2o_flag,
    o3_flag=o3_flag,
    blackbody=h_start_blackbody_surface,
    res=res)