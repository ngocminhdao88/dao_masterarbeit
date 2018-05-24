"""
Plot the curve and try to use RectangleSelector from matplotlib library

Usage:
    python plot_curve_v2.py -i <file_name>
"""

import sys
import getopt
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.widgets import RectangleSelector


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
    """
    u_0 = 0.2  # charge voltage [V]
    delta_t = max(x_array) - min(x_array)  # time [s]
    u_1 = min(y_array)  # start voltage [V]
    u_2 = max(y_array)  # end voltage [V]

    # time constant of the charging capacitor
    tau = delta_t / np.log((u_2 / u_0) / (u_1 / u_0))

    return tau


def getInfoFromHeader(work_file):
    """
    Read the header from test file and extract it's information.
    A line holds the infomation has those format
        Info: blah blah blah

    Input:
        work_file (str): path to working file
    Output:
        info (str): extracted information from the header
    """
    f = open(work_file, 'r', encoding="utf-8", errors="ignore")
    info = ""

    for line in f:
        if "Info" in line:
            temp = line.split(':', maxsplit=1)
            # get the infomation and strip all unwanted whitespaces
            info = temp[1].strip()

            break  # done, exit the for loop

    f.close()  # close the file when done with it

    return info


def line_select_callback(eclick, erelease, fig, ax):
    """
    Processing the event when the user drag and select a region on the plot
    """
    # get the coordinate of drew rectangle
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    # get the line, point and text in ax
    line = ax.lines[0]
    line_fit = ax.lines[1]
    point = ax.lines[2]
    text = ax.texts[0]

    # get all datas from the line on the plot
    x_data = line.get_xdata()
    y_data = line.get_ydata()

    # masking the datas from line in range of drew rectangle
    mask = (x_data > min(x1, x2)) & (x_data < max(x1, x2)) & \
           (y_data > min(y1, y2)) & (y_data < max(y1, y2))

    # get the data from line using the mask
    x_masked = x_data[mask]
    y_masked = y_data[mask]

    # offset the time and the charging voltate (y axis)
    x_masked_offset = x_masked - x_masked[0]
    y_masked_offset = y_masked - y_masked[0]

    # processing the data if in drew rectangle
    if len(x_masked) > 0:
        # positon to draw the text (at maximum)
        xmax = x_masked[np.argmax(y_masked)]
        ymax = y_masked.max()

        # try to fit the selected data
        popt, pcov = curve_fit(chargeFuntion, x_masked_offset, y_masked_offset)

        # calculate tau and capacitance
        tau = popt[0]
        cap = getCapacitance(tau)

        # build the text
        tx = "tau = %e\nc = %e" % (tau, cap)
        print(np.sqrt(np.diag(pcov)))

        point.set_data([xmax], [ymax])
        text.set_text(tx)
        text.set_position((xmax, ymax))

        # plot the fited curve
        y_fited = chargeFuntion(x_masked_offset, tau) + y_masked[0]
        line_fit.set_data(x_masked, y_fited)

        fig.canvas.draw_idle()


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

    info = getInfoFromHeader(work_file)
    # read data from the tenth line and use first col as index
    data = pd.read_csv(work_file, sep='\t', skiprows=10, index_col=0)
    num_elements = len(data.iloc[:, 0])
    time_ax = np.arange(0, num_elements)
    time_ax = time_ax * 4e-6  # [s]; 4us per sample

    for curve in data.columns.values:
        # setup the plot figure and axis
        fig, ax = plt.subplots()
        ax.set_title(info + '\n' + str(curve) + '\n' + work_file)
        line, = ax.plot(time_ax, data[curve], linewidth="0.5", label="data")
        line_fit, = ax.plot([], [], "r-", linewidth="0.5")
        point, = ax.plot([], [], marker="o", color="crimson")
        text = ax.text(0, 0, "")

        # connecting the event handler with the draw rectangle event on the plot
        rs = RectangleSelector(ax, lambda eclick, erelease, fig=fig, ax=ax:
                               line_select_callback(eclick, erelease, fig, ax),
                               drawtype='box', useblit=False, button=[1], 
                               minspanx=5, minspany=5, spancoords='pixels', 
                               interactive=True)
        plt.xlabel("Time [s]")
        plt.ylabel("Spannung [V]")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
