"""
Plot the histogram of all capacitance

Usage:
    python capacitance_histogram.py -i <file_name>
"""

import sys
import getopt
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector


class MeasurementData:
    """
    Class to hold data of the measurement
    """
    def __init__(self, work_file):
        self.data_list = []
        self.data_temp = 0
        self.work_file = work_file
        self.header = self.readHeader()
        self.info = self.readInfo()

    def addTempData(self, value):
        self.data_temp = value

    def addData(self):
        self.data_list.append(self.data_temp)

    def getData(self):
        return self.data_list

    def getWorkFile(self):
        return self.work_file

    def readInfo(self):
        """
        Read the user's information in header

        Output:
            info (str): user's information
        """
        temp = self.header.split('\n')
        info = [s for s in temp if "Info" in s]

        return info[0]

    def getInfo(self):
        """
        Return user's information of this test
        """
        return self.info

    def readHeader(self):
        """
        Read the header from this measurement file
        """
        # open the work file
        if os.path.isfile(self.work_file):
            f = open(self.work_file, 'r')
        else:
            assert False, "File not exist"

        header = []
        header_str = ""
        temp_line = ""

        while "Capacitance" not in temp_line:
            temp_line = f.readline()

            # skip the blank line
            if len(temp_line) > 1:
                header.append(temp_line)

        header = header[:-1]  # remove last item in the header

        # build the header
        for line in header:
            header_str += line

        # close the file when done with it
        f.close()

        return header_str

    def getHeader(self):
        """
        Return the header of this test
        """
        return self.header


def chargeFuntion(t, tau):

    """
    Calculate the charing voltage of a capacitor

    Input:
        t (float): time
        tau (float): time constant
    """
    u0 = 0.2  # charge voltage [V]

    return u0 * (1 - np.exp(-t / tau))


def usage():
    """
    Print out the help how to use this file
    """
    print(__doc__)


def getCapacitance(tau):
    """
    Calculate the capacitance using the it's charging time constant
    and charging resistor

    Input:
        tau (float): time constant

    Output:
        c (float): capacitance
    """
    r_v = 10000000  # charge resistor [Ohm]
    # r_v = 1012700  # charge resistor [Ohm]
    c = tau * (1 / r_v)  # capacitance

    return c


def getTau(x_array, y_array):
    """
    Calculate the tau from a capacitor charge curve

    Input:
        x_array (array): time
        y_array (array): voltage

    Output:
        tau (float): time constant of the charging capacitor
        time_offset (float): an offset to trace back the start of a function
    """
    u_0 = 0.2  # charge voltage [V]
    delta_t = max(x_array) - min(x_array)  # time [s]
    u_1 = min(y_array)  # start voltage [V]
    u_2 = max(y_array)  # end voltage [V]

    # time constant of the charging capacitor
    tau = delta_t / np.log((u_0 - u_1) / (u_0 - u_2))

    # time offset to the start of function
    time_offset = tau * np.log((u_0 - u_1) / u_0)

    return (tau, time_offset)


def main(argv):
    # get the commandline options
    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "input="])
    except getopt.GetoptError:
        sys.exit(2)

    # parse the options and arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            work_file = arg  # name of working file
        else:
            assert False, "wrong option"

    # all the test information are stored in here
    my_data = MeasurementData(work_file)

    # read data from the tenth line and use first col as index
    data = pd.read_csv(work_file, sep='\t', skiprows=10)

    capacitance = data["Capacitance"] * 1e12  # scale cap to pF
    cable_cap = 100  # [pF]
    capacitance = capacitance - cable_cap

    data_sigma = np.std(capacitance)
    data_mean = np.mean(capacitance)
    bins = 50

    print("mean: %f, sigma: %f" % (data_mean, data_sigma))

    # setup the plot
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(capacitance, bins=bins, facecolor="green",
                               edgecolor="black", linewidth=0.5, density=1)

    # add a 'best fit' line
    y = ((1 / (np.sqrt(2 * np.pi) * data_sigma)) *
         np.exp(-0.5 * (1 / data_sigma * (bins - data_mean))**2))
    ax.plot(bins, y, '--')

    ax.set_xlabel("Cap [pF]")
    ax.set_ylabel("Probability")
    ax.set_title(my_data.getInfo())

    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
