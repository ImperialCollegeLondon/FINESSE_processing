"""Functions to write lblrtm tape 5 files for different cases, run lblrtm and read output
Authour: Laura Warwick
Written 15/05/2019
Edited: 06/06/2019: Clarified with print statement if calculating transmission or radiance
                    Edited to run optical depths also
Edited: 23/06/2020: Can now prescribe continuum
"""

import math as math

import numpy as np


def write_tape5(
    pro_z,
    pro_p,
    pro_t,
    pro_q,
    h_start_temp,
    h_obs,
    h_start,
    wn_range,
    angle,
    atm,
    mode,
    pro_oco=None,
    pro_o3=None,
    pro_n2o=None,
    pro_co=None,
    pro_ch4=None,
    pro_so2=None,
    pro_no2=None,
    t5="TAPE5",
    h2o_flag="A",
    o3_flag="A",
    yaxis_flag="P",
    path_length=None,
    horizontal=2,
    blackbody=True,
    od=0,
    res=0.01,
    continuum=False,
    n_species=14,
):  # res=0.001
    """; AUTO_TAPE5 procedure for auto-generation of LBLRTM TAPE5 input file
    ; Takes as input user defined atmospheric profile and options
    ; Produces LBLRTM TAPE5 file for line-by-line radiance calculation
    ; Version 1.0 coded by Stu Newman, 06.01.2009
    ; Version 1.1 (SMN) 15.01.2009 - introduce scaling of continuum species as an option
    ; Version 1.2 (SMN) 23.01.2009 - minor bugfix where trace gases not specified
    ; Version 1.3 (SMN) 17.03.2009 - /tau keyword to output transmittance rather than radiance
    ; Version 1.4 (SMN) 26.11.2009 - corrected major bug in naming of CFC species (F11, F12)
    ; Version 1.5 (SMN) 08.12.2009 - bugfix for different standard atmospheres
    ;
    ; Edited: R Bantges (Aug 2013)
    ; - Renamed auto_tape5 to write_lblrtm_tape5_v2
    ; - Reformatted and commented
    ; - Edited to suit the specific radiosonde type simulation observations

    ; Edited: HEB (Oct 2015)
    ; - to include updated gas profiles
    ; - for Greenland emissivity work

    ; Edited LRW (Jan 2019)
    ; - to take watervapour information in humidity or ppmv
    ; - specify boundries in terms of height
    ; - added capacity to specify number of levels
    ; - to allow for scaling of continuum
    ;
    ; Edited SP (May 2025)
    ; - edits to integrate into modular FINESSE running code
    ; - included variable for either pressure or altitude input
    INPUTS:
    pro_z       = atmospheric hights (km)
    pro_p       = atmospheric pressure profile (hPa)
    pro_t       = atmospheric temperature profile (K)
    pro_q       = atmospheric humidity profile (%) or h2o in ppmv
                    (make sure you check flag in jchar)
    h_start_temp= temperature for boundary at which radiance calculation
                    begins (2.7 K for zenith downwelling (deep space)
                    surface skin temperature for upwelling radiation)
    h_obs       = height where observation of radiance takes place
                    (for example aircraft height) (km)
    h_start     = height from which radiance is to be calculated (km)
    wn_range    = wavenumber range [V1,V2], e.g. [500., 2000.],
                    (for LBLRTM<=12.8 require V2-V1 < 2020 cm^-1)
    angle       = zenith angle at observer altitude,
                    in LBLRTM 180. is upwelling or nadir,
                    0. is downwelling or zenith
    atm         = model atmosphere for unspecified species
                  1 => tropical model
                  2 => midlatitude summer model
                  3 => midlatitude winter model
                  4 => subarctic summer model
                  5 => subarctic winter model
                  6 => U.S. standard 1976
    mode        = specifies if running in transmission 0, or radiance 1
    ; KEYWORDS:
    pro_co      = (optional) atmospheric CO profile (ppmv)
    pro_oco     = (optional) atmospheric CO2 profile (ppmv)
    pro_o3      = (optional) atmospheric O3 profile (ppmv)
    pro_ch4     = (optional) atmospheric CH4 profile (ppmv)
    pro_n2o     = (optional) atmospheric N2O profile (ppmv)
    pro_no2     = (optional) atmospheric NO2 profile (ppmv)
    pro_so2     = (optional) atmospheric SO2 profile (ppmv)
    t5          = output file name (including path) for TAPE5 file
    h2o flag    = specify 'H' for relative humidity,
                    'C' for mass mixing ratio (g/kg),
                    else ppmv selected using 'A'
    yaxis_flag  = specify 'A' for altitude,
                    else 'P' for pressure is used
    horizontal  = 2 for slant path,
                    1 for horizontal path.
                    Default is slant.
    path_length = length for horizontal path in km.
                    Only neede if horizontal=1
    blackbody   = True by default assumes blackbody,
                    to read emissivity from file set to False
    OD          = specifies if writing out seperate optical depth files
                    (0 = no, 1 = yes)
    res         = resolution of output spectrum
    continuum   = scaling factors for water vapour continuum in form
                  [H2O self broadened, H2O foreign broadened,
                  CO2 continuum, O3 continuum,
                   O2 continuum, N2 continuum,
                   Rayleigh extinction]
                   If False standard contimuum is used. Deafult is False.
    n_species   = Number of atmospheric species to include in simulation
                    see line 168 for list of species. Deafult is 14
                    (LW: this file was given to me with 14 species set I don't
                    know if it is the best choice!!)
    """
    n_levels = len(pro_z)
    print("========== Inputs ==========")
    if yaxis_flag == "P":
        print("Using pressure input (hPa)")
    else:
        print("Using altitude input (km)")
    print("Number of levels in full profile", n_levels)
    print("Wavenumbe range and resolution: ", wn_range, res)
    print("View angle: " + str(angle) + " deg ")
    print("View altitude/pressure: " + str(h_obs))
    # specify standard atmosphere
    atm = str(int(atm))

    # set default settings to override incase incorrect entry

    if angle == 0:
        h_start_blackbody_surface = True
        h_start_temp = 2.7  # temperature at h_start

    if h_start_blackbody_surface == False:
        "Running with emissivity file. EMISSIVITY and REFLECTIVTIY files must be in executable directory."

    # specify flags for selected profiles
    oco_flag = atm
    n2o_flag = atm
    co_flag = atm
    ch4_flag = atm
    so2_flag = atm
    no2_flag = atm

    if isinstance(pro_oco, (list, tuple, np.ndarray)):
        oco_flag = "A"
        pro_oco = np.asarray(pro_oco)
    else:
        pro_oco = np.zeros(n_levels)
        # pro_oco = None

    if isinstance(pro_o3, (list, tuple, np.ndarray)):
        o3_flag = "C"
        pro_o3 = np.asarray(pro_o3)
    else:
        pro_o3 = np.zeros(n_levels)

    if isinstance(pro_n2o, (list, tuple, np.ndarray)):
        n2o_flag = "A"
        pro_n2o = np.asarray(pro_n2o)
    else:
        pro_n2o = np.zeros(n_levels)
        # pro_n2o = None

    if isinstance(pro_co, (list, tuple, np.ndarray)):
        co_flag = "A"
        pro_co = np.asarray(pro_co)
    else:
        pro_co = np.zeros(n_levels)
        # pro_co = None

    if isinstance(pro_ch4, (list, tuple, np.ndarray)):
        ch4_flag = "A"
        pro_ch4 = np.asarray(pro_ch4)
    else:
        pro_ch4 = np.zeros(n_levels)
        # pro_ch4 = None

    if isinstance(pro_so2, (list, tuple, np.ndarray)):
        so2_flag = "A"
        pro_so2 = np.asarray(pro_so2)
    else:
        pro_so2 = np.zeros(n_levels)
        # pro_so2 = None

    if isinstance(pro_no2, (list, tuple, np.ndarray)):
        no2_flag = "A"
        pro_no2 = np.asarray(pro_no2)
    else:
        pro_no2 = np.zeros(n_levels)
        # pro_no2 = None

    # ; Define flags for units and input options, molecular IDs are
    # ; (1)=H2O (2)=CO2 (3)=O3 (4)=N2O (5)=CO (6)=CH4 (7)=O2 (8)=NO
    # ; (9)=SO2 (10)=NO2 (11)=NH3 (12)=HNO3 (13)=OH (14)=HF (15)=HCL (16)=HBR
    # ; (17)= HI (18)=CLO (19)=OCS (20)=H2CO (21)=HOCL (22)=N2 (23)=HCN (24)=CH3CL
    # ; (25)=H2O2 (26)=C2H2 (27)=C2H6 (28)=PH3 (29)=COF2 (30)=SF6 (31)=H2S (32)=HCOOH
    # ; (33)=HO2 (34)=O (35)=CLONO2 (36)=NO+ (37)=HOBR (38)=C2H4 (39)=CH3OH
    # ;
    # ; Note that thesis work suggests that CCl4, NO2, and SO2 may be possible to 'see' in window
    # ; suspect other gas effects will be masked, at least in nadir view
    # ;
    # ; Assume that water vapour is always defined, others are optional

    jchar_other = atm * 17 + " "
    jchar = (
        h2o_flag
        + oco_flag
        + o3_flag
        + n2o_flag
        + co_flag
        + ch4_flag
        + atm
        + atm
        + so2_flag
        + no2_flag
        + jchar_other
    )
    CFCs = ["CCL4", "F11", "F12", "CHCLF2", "CF4"]
    # Define wn range
    wn1 = wn_range[0]
    wn2 = wn_range[1]

    # Set altitude or pressure run
    if yaxis_flag == "A":
        yaxis_var = 1
    else:
        yaxis_var = -1

    print("========== Writing TAPE5 ==========")
    with open(t5, "w+") as file:
        file.write("$ TAPE5 generated by write_tape5 in write_tape5.py\n")

        # **Record 1.2**
        # (RJB): SC = 2 to enable "INTRPL" - interpolating procedure (RECORD 9.1) (default was SC=0)
        # If using standard continuum
        if not continuum:
            file.write(
                f" HI=1 F4=1 CN=1 AE=0 EM=1 SC=2 FI=0 PL=0 TS=0 AM=1 MG=0 LA=0 OD={od:1d} XS=0   00   00\n"
            )
        else:
            # To specify scaling on continuum
            file.write(
                f" HI=1 F4=1 CN=6 AE=0 EM=1 SC=2 FI=0 PL=0 TS=0 AM=1 MG=0 LA=0 OD={od:1d} XS=0   00   00\n"
            )
            file.write(
                "{:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f}\n".format(*continuum)
            )
            print("Continuum scaling")
        # ** Record 1.3 **
        file.write(
            "{:10.3E}{:10.3E}{:>40s}{:10.3E}{:10.3E}".format(
                wn1, wn2, " ", 0.0002, 0.001
            )
        )
        if od == 0:
            file.write("\n")
        if od == 1:
            file.write("REJ=0     0.025\n")

        # ** Record 1.4 **
        # first value is temp of boundary, second value is emissivity, set to < 0 for routine to read 'EMISSIVITY'
        # and 'REFLECTIVITY' file
        if blackbody:
            print("Assuming blackbody")
            file.write(
                "{:10.3f}{:10.3f}{:>20s}{:10.3f}\n".format(h_start_temp, 1, "", 0.0)
            )
        else:
            print("Taking emissivity from file")
            file.write(
                "{:10.3f}{:10.3f}{:>20s}{:10.3f}\n".format(h_start_temp, -1, "", -1)
            )

        # ** Record 3.1 **
        # (if IATM is set - AM=1) query zbound
        # (LRW) Change between user specified and standard atmosphere here
        file.write(
            f"{0:5d}{horizontal:5d}{-1*n_levels:5d}{1:5d}{1:5d}{n_species:5d}{1:5d}{0:2d} {0:2d}{0:10.3f}{100.:10.3f}\n"
        )
        # user atm, specified path , molecular species

        if horizontal == 2:
            print("Running in vertical mode")
            # ** Record 3.2 ** - top and bottom height unless IBMAX < 0
            file.write(f"{h_obs:10.3f}{h_start:10.3f}{angle:10.3f}\n")

        # ** Record 3.3b **
        # for i in range(math.ceil(n_levels / 5)):
        #     values = pro_p[(i*5):((i+1)*5)]
        #     file.write("{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}\\n".
        #                format(values[0], values[1], values[2], values[3], values[4]))

        # ** Record 3.3b **
        for i in range(math.ceil(n_levels / 8)):
            values = pro_p[(i * 8) : ((i + 1) * 8)]
            file.write("".join([f"{v:10.3f}" for v in values]) + "\n")  # you're welcome

        #         # ** Record 3.3b **
        # for i in range(math.ceil(n_levels / 8)):
        #     values = pro_p[(i*8):((i+1)*8)]
        #     file.write("{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}\n".
        #                format(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7]))

        # ** Record 3.4 **
        file.write("{:5d}{:>24s}\n".format(yaxis_var * n_levels, "  LBL PROFILE"))

        # ** Record 3.5 **
        for j in range(n_levels):
            # (NB: heights set to zero, only first entry needs to be surface value)
            # L indicates units for majority of molecules (vmr)
            file.write(
                "{:10.3f}{:10.3f}{:10.3f}     {:1s}{:1s} {:1s} {:>28s}\n".format(
                    pro_z[j], pro_p[j], pro_t[j], "A", "A", "L", jchar
                )
            )
            # ** Record 3.6.n **
            file.write(
                f"{pro_q[j]:15.8E}{pro_oco[j]:15.8E}{pro_o3[j]:15.8E}{pro_n2o[j]:15.8E}{pro_co[j]:15.8E}{pro_ch4[j]:15.8E}{0.0:15.8E}\n"
            )
            file.write(
                f"{0.0:15.8E}{pro_so2[j]:15.8E}{pro_no2[j]:15.8E}{0.0:15.8E}{0.0:15.8E}{0.0:15.8E}{0.0:15.8E}{0.0:15.8E}{0.0:15.8E}"
                + "\n"
            )
        # ** Record 3.7 **
        # (if IATM is set - AM=1 AND IXSECT (XS)= 1) query zbound
        # (SP) Adding in the CFCs and cross section molecules for a standard atmosphere (I5 is intenger)
        file.write(f"{len(CFCs):5d}{0:5d}{0:5d}\n")
        # n.o cross section molecules, standard profile, deselect pressure convolution of cross-sections

        # ** Record 3.7.1 **
        # name of molecules to be used(XSNAME(I)), I=1, IXMOLS
        # for k in range(len(CFCs)):
        #    file.write("{:10s}".format(CFCs[k]))
        # file.write("\n")

        # ** Record 3.8 **
        # file.write("{:5d}{:5d}{:>50}\n".format(n_levels,1,'  LBL CFC PROFILE'))

        # ** Record 3.8.1 **
        # for l in range(n_levels):
        #    file.write("{:10.3f}     {:>35s}\n"
        #               .format(pro_p[l], 'A A A A'))

        # ** Record 3.6.n **
        #    file.write("{:10.3E}{:10.3E}{:10.3E}{:10.3E}{:10.3E}\n"
        #              .format(9.010E-05, 2.402E-04, 5.404E-04, 2.000E-04,9E-05))

        # **Record 9.1**
        # Extend wavenumber range slightly to avoid numerical errors
        # Appears it is necessary to avoid unit numbers 55 and 66 for output
        # TAPE12 is default LBL output, interpolate to TAPE11
        file.write(
            f"{res:10.3F}{wn1 - .01:10.3F}{wn2 + .01:10.3F}{mode:5d}{0:5d}               {12:5d}          {11:5d}\n"
        )
        if mode == 0:
            print("Calculating Transmission")
        if mode == 1:
            print("Calculating Radiances Only")
        file.write("-1.\n")  # (RJB) This will terminate the interpolation
        file.write("%%%%%")
    return
