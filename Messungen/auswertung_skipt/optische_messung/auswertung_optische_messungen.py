# -*- coding: utf-8 -*-
"""
Plot the film thickness over speed of the measurement on PCS test rig at VW

Usage:
    python auswertung_optische_messungen.py --input=<filename>
"""

import sys, getopt, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

def usage():
    print(__doc__)

def getTestParams(work_file):
    test_params = ""
    # read the header in the measurement file
    f = open(work_file, 'r', encoding='utf-8', errors='ignore') # open to read working file
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

# get the commandline options
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "input="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # parse the options and arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            work_file = arg # name of working file
        else:
            assert False, 'wrong options'
    
    test_params = getTestParams(work_file)
    
    data_frame = pd.read_csv(work_file, skiprows=10, header=0, sep='\t')
    # strip all white spaces in header replace it with underscore
    columns_temp = data_frame.columns.values
    for i, col in enumerate(columns_temp):
        # strip all leading and ending whitespaces
        col = col.strip()
        # replace all whitespaces with a single underscore
        col = re.sub(r"\s+", '_', col)
        # replace the new header with the old
        columns_temp[i] = col
    
    data_frame.columns = columns_temp
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(test_params)
    ax.set_xlabel("Speed [m/s]")
    ax.set_ylabel("Film [nm]")
    line, = ax.plot(data_frame["Disc_Speed"], data_frame["Film"], 'o')

    fig_name = work_file + ".png"
    fig.savefig(fig_name, bbox_inches='tight')
    
if __name__ == "__main__":
    main(sys.argv[1:])