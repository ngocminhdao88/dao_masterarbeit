# -*- coding: utf-8 -*-
"""
Plot the film thickness over speed of the measurement on PCS test rig at VW

Usage:
    python auswertung_optische_messungen.py --input=<filename>
"""

import sys
import getopt
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import theory_film_capacitance_fva3 as theory_film


def usage():
    print(__doc__)


def getTestParams(work_file):
    test_params = ""

    # open to read working file
    f = open(work_file, 'r', encoding='utf-8', errors='ignore')

    for line in f:
        # find the Comments line
        if "Comments" in line:
            # remove the "Comments" from the line
            line = line.replace("Comments", '')
            # remove all the whitespaces
            line = re.sub(r"\s+", '', line)
            test_params = line

    f.close()

    return test_params


work_file_1 = "fva3_T40_F20.dat"
work_file_2 = "fva3_T40_F20_ref.dat"

test_params_1 = getTestParams(work_file_1)
test_params_2 = getTestParams(work_file_2)

data_frame_1 = pd.read_csv(work_file_1, skiprows=10, header=0, sep='\t')
data_frame_2 = pd.read_csv(work_file_2, skiprows=10, header=0, sep='\t')

# strip all white spaces in header replace it with underscore
columns_temp = data_frame_1.columns.values
for i, col in enumerate(columns_temp):
    # strip all leading and ending whitespaces
    col = col.strip()
    # replace all whitespaces with a single underscore
    col = re.sub(r"\s+", '_', col)
    # replace the new header with the old
    columns_temp[i] = col

data_frame_1.columns = columns_temp

# strip all white spaces in header replace it with underscore
columns_temp = data_frame_2.columns.values
for i, col in enumerate(columns_temp):
    # strip all leading and ending whitespaces
    col = col.strip()
    # replace all whitespaces with a single underscore
    col = re.sub(r"\s+", '_', col)
    # replace the new header with the old
    columns_temp[i] = col

data_frame_2.columns = columns_temp

# get data from theory_film module
data_theory_40C_20N = theory_film.data_40C_20N

fig = plt.figure(figsize=[5, 3.125])
ax = fig.add_subplot(111)

line_1, = ax.plot(data_frame_1["Disc_Speed"], data_frame_1["Film"],
                  'o', label="T40,F20")
line_2, = ax.plot(data_frame_2["Disc_Speed"], data_frame_2["Film"],
                  '^', label="Ref,T40,F20")
line_3, = ax.plot(data_theory_40C_20N["Speed"], data_theory_40C_20N["Film"] * 1e9,
                  label="Theorie,T40,F20")

ax.set_xlabel("Speed [m/s]")
ax.set_ylabel("Film [nm]")
ax.set_xlim(0, 1.5)
ax.set_ylim(0, 650)
ax.legend()

fig.tight_layout()
fig_name = "vergleichsmessung_T40_F20_FVA3.pdf"
fig.savefig(fig_name, bbox_inches="tight", pad_inches=0)

plt.show()
