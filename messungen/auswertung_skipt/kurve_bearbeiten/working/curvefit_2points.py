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

        while "Kurve" not in temp_line:
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


def saveData(my_data):
    """
    Save the capacitance from fitted curve in to a file
    """
    # create a data folder to hold the new files there
    if not os.path.isdir("data"):
        print("data folder is not found. Create it\n")
        os.mkdir("data")

    # get the name and it's extension of work file
    file_name, file_ext = os.path.splitext(my_data.getWorkFile())

    # build new file name
    work_file = "./data/" + file_name + "_data" + file_ext

    # get the test informaiton
    header = my_data.getHeader()

    # open the work file
    f = open(work_file, 'w')

    # write down the filename and test's information
    f.write(header)
    f.write("Capacitance\n")

    # write down the capacitance from fitted curve in the file
    for data in my_data.getData():
        f.write(str(data) + '\n')

    # close the work file
    f.close()


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
    # r_v = 10000000  # charge resistor [Ohm]
    r_v = 1012700  # charge resistor [Ohm]
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


def line_select_callback(eclick, erelease, fig, ax, my_data):
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

    # processing the data if in drew rectangle
    if len(x_masked) > 0:
        # positon to draw the text (at maximum)
        xmax = x_masked[np.argmax(y_masked)]
        ymax = y_masked.max()

        # calculate the time constant und the capacitance
        tau, time_offset = getTau(x_masked, y_masked)
        cap = getCapacitance(tau)

        # add temporary data in to the storage
        my_data.addTempData(cap)

        # time, where the charging function begin
        time_start = x_masked[0] + time_offset

        # time data to calculate the charing function
        new_mask = x_data > time_start
        time = x_data[new_mask]
        time = np.arange(0, len(time)) * 4e-6

        # calculate data for fitted curve
        y_fited = chargeFuntion(time, tau)

        # plot the fitted curve at its root
        line_fit.set_data(time + time_start, y_fited)

        # print the information at maximum
        tx = "tau = %e\nc = %e" % (tau, cap)
        point.set_data([xmax], [ymax])
        text.set_text(tx)
        text.set_position((xmax, ymax))

        # draw the fitted curve and text on screen
        fig.canvas.draw_idle()


def pressEventHandler(event, my_data):
    """
    Handle the event when user press a key on plot.
    Save the capacitance from the fitted curve to process later
    """

    if event.key == 'y':
        my_data.addData()


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
    data = pd.read_csv(work_file, sep='\t', skiprows=10, index_col=0)

    # build the time axis
    num_elements = len(data.iloc[:, 0])
    time_ax = np.arange(0, num_elements)
    time_ax = time_ax * 4e-6  # [s]; 4us per sample

    for curve in data.columns.values:
        # setup the plot figure and axis
        fig, ax = plt.subplots()
        ax.set_title(my_data.getInfo() + '\n' +
                     str(curve) + '\n' + my_data.getWorkFile())
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Voltage [V]")
        ax.set_ylim(0, 0.22)
        ax.yaxis.grid(True)

        # place holder for datas in plot
        line, = ax.plot(time_ax, data[curve], linewidth="0.5")
        line_fit, = ax.plot([], [], "r-", linewidth="0.5")
        point, = ax.plot([], [], marker="o", color="crimson")
        text = ax.text(0, 0, "")

        # connecting the event handler with key press
        fig.canvas.mpl_connect('key_press_event',
                               lambda event, my_data=my_data:
                               pressEventHandler(event, my_data))

        # fig window at top left corner
        fig.canvas.manager.window.move(0,0)

        # connecting the event handler with the draw rectangle event on the plot
        rs = RectangleSelector(ax, lambda eclick, erelease, fig=fig, ax=ax, my_data=my_data:
                               line_select_callback(eclick, erelease, fig, ax, my_data),
                               drawtype='box', useblit=False, button=[1],
                               minspanx=5, minspany=5, spancoords='pixels',
                               interactive=True)

        plt.show()

    # save the processed data in to the file
    if len(my_data.getData()) > 0:
        saveData(my_data)

if __name__ == "__main__":
    main(sys.argv[1:])
