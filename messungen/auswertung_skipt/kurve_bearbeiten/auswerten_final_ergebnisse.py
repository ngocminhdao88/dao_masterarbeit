"""
Read datas from the final result excel sheet and plot it
"""

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import matplotlib.pyplot as plt


work_file = "messergebnisse_kapazitaet.xlsx"
fig_file = "cap_vs_speed_meas.pdf"

# read data from excel file
data_40C = pd.read_excel(work_file, sheet_name="FVA3_40C_20N")
data_60C = pd.read_excel(work_file, sheet_name="FVA3_60C_20N")
data_80C = pd.read_excel(work_file, sheet_name="FVA3_80C_20N")

# # plot measured capacitance vs speed with different temp
# fig, ax = plt.subplots()
#
# # plot cap vs speed
# ax.plot(data_40C["Speed"], data_40C["Cap"], 's-', label="40C")
# ax.plot(data_60C["Speed"], data_60C["Cap"], 'D-', label="60C")
# ax.plot(data_80C["Speed"], data_80C["Cap"], '^-', label="80C")
#
# ax.set_xlabel("Speed [m/s]")
# ax.set_ylabel("Cap [pF]")
# ax.legend()
#
# fig.tight_layout()
#
# # export the fig to pdf
# # fig.savefig(fig_file, bbox_inches="tight", pad_inches=0)
#
# plt.show()

# plot measured cap and theory cap vs speed
fig, ax = plt.subplots(figsize=[5, 3.125])

# plot cap vs speed
ax.plot(data_80C["Speed"], data_80C["Cap"], 's-', label="C_gemessen,80C")
ax.plot(data_80C["Speed"], data_80C["Cap_theory_pf"], '^-', label="C_berechnet,80C")

ax2 = ax.twinx()
ax2.plot(data_80C["Speed"], data_80C["Film"], '*-', color='g')
ax2.set_ylabel("Film [nm]", color='g')
ax2.tick_params('y', colors='g')

ax.set_xlabel("Speed [m/s]")
ax.set_ylabel("Cap [pF]")
ax.legend(loc=9)

fig.tight_layout()

# export the fig to pdf
fig.savefig("cap_theo_meas_vs_speed_80C.pdf", bbox_inches="tight", pad_inches=0)

plt.show()
