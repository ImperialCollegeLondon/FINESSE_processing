"""
Plot data from the GUI logger and vaisala instumentation

Note this is for GUI data so it can be used in both single and multi cases
"""

from matplotlib import pyplot as plt
import calibration_functions_sanjee as cal

DATE = "20230220"
PATH = '/disk1/Andoya/sp1016/'

DATA_LOCATION = PATH+f"Raw_Data/{DATE}/"
GUI_DATA_LOCATION = DATA_LOCATION + "clear_sky1-20230220103722.log"
PTH_DATA_LOCATION = DATA_LOCATION + "PTH_all.txt"
CO2_DATA_LOCATION = DATA_LOCATION + "CO2_all.txt"

PATH2 = '/disk1/sm4219/GIT/FINESSE_CAL/'
SAVE_LOACTION = PATH2+f"Processed_Data_soph_single/{DATE}/"

if DATE == "20230217":
    time_lims = [20000, 48000]  # 20230217
elif DATE == "20230220":
    time_lims = [35000, 52500]  # 20230220
elif DATE == "20230221":
    time_lims = [50000, 80000]  # 20230221
elif DATE == "20230222":
    time_lims = [17500, 35000]  # 20230222
gui_data = cal.load_gui(GUI_DATA_LOCATION)
print("DATA LOCTAION HERE:", PTH_DATA_LOCATION)
pth_time, pth_pressure, pth_temp, pth_humidity = cal.load_pth(
    PTH_DATA_LOCATION)


cal.update_figure(5, [8, 7])
axes_labels = ["(a)", "(b)", "(c)", "(d)"]
label_location = (0.05, 0.95)

fig1, axs1 = plt.subplots(2, 2, sharex=True)

axs1[0, 0].plot(gui_data["time"], gui_data["HBB"], label="HBB temperature")
axs1a = axs1[0, 0].twinx()
axs1a.plot(gui_data["time"], gui_data["HBB"],
           label="Hot BB temperature (C)", color="g")
axs1[0, 0].set(
    xlim=time_lims,
    ylabel="Hot BB temperature (C)")
axs1a.set_ylabel("Hot BB temperature (C)", color="g")
axs1a.set_ylim([69, 71])
axs1a.tick_params(axis="y", labelcolor="g")

axs1[0, 1].plot(gui_data["time"], gui_data["CBB"], label="CBB temperature")
# axs1b = axs1[0, 1].twinx()
# axs1b.plot(
# gui_data["time"], gui_data["CBB"], label="Cold BB temperature (C)", color="g"
# )
axs1[0, 1].set(
    xlim=time_lims,
    ylabel="Cold BB temperature (C)")
# axs1b.set_ylabel("Cold BB temperature (C)", color="g")
# axs1b.set_ylim([31, 31.5])
# axs1b.tick_params(axis="y", labelcolor="g")

axs1[1, 0].plot(gui_data["time"], gui_data["PRT1"], label="PRT1 - Front of electronics box")
axs1[1, 0].plot(gui_data["time"], gui_data["PRT2"], label="PRT2 - On the ground")
axs1[1, 0].plot(gui_data["time"], gui_data["PRT3"], label="PRT3 - Top of EM27")
axs1[1, 0].plot(gui_data["time"], gui_data["PRT4"], label="PRT4 - Stepper Motor")
axs1[1, 0].set(
    xlim=time_lims,
    xlabel="Time since midnight (s)", 
    ylabel="Monitoring Temperatures (K)",
    ylim=[-7, 30]
)
axs1[1, 0].legend(prop={'size': 7}, loc='upper right')

axs1[1, 1].plot(pth_time, pth_temp, label="Air temperature")
axs1d = axs1[1, 1].twinx()
axs1d.plot(pth_time, pth_humidity, label="Humidity", color="g")
axs1[1, 1].set(
    xlabel="Time since midnight (s)",
    ylabel="Air temperature (C)",
    xlim=axs1[0, 0].get_xlim(),
)
axs1d.set_ylabel("Humidity (%)", color="g")
axs1d.tick_params(axis="y", labelcolor="g")

for i, ax in enumerate(axs1.flatten()):
    ax.grid()
    ax.annotate(axes_labels[i], label_location, xycoords='axes fraction')

fig1.tight_layout(pad=2)
fig1.savefig(SAVE_LOACTION + "Summary.png")
plt.show()
