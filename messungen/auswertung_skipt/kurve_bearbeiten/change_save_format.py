"""
Change the format of the save datas from the program Ladekurve_mobil.
Old format is one column all all the curve, new format is all the curves in
tab seperate columns.
The new files will be saved in the new_format folder

Usage:
    python change_save_format.py --input=<file_name>
"""
import sys
import getopt
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def usage():
    """
    Print out the help message
    """
    print(__doc__)


def saveData(file_name, dataframe, header):
    """ Save data of the dataframe in to the new file

        Input:
            file_name (str): name of the temp file
            dataframe (pandas DataFrame): all the curves
            header (list): measurement infomation
    """

    # create a tmp folder to hold the files
    if not os.path.isdir('new_format'):
        print('new_format folder not found. Create it\n')
        os.mkdir('new_format')

    # build the path
    file_name = './new_format/' + file_name

    f = open(file_name, 'w')  # create tmp file to hold data

    # write the header before the 1st curve
    for data in header:
        f.write("%s" % data)
    f.close()

    # write the data of the dataframe in to the existing file
    dataframe.to_csv(file_name, sep='\t', mode='a')


def main(argv):
    # get the commandline options
    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "input="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # parse the options and arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(2)
        elif opt in ("-i", "--input"):
            work_file = arg  # name of working file
        else:
            assert False, 'error when parsing the input options'

    # open to read working file
    f = open(work_file, 'r', encoding='utf-8', errors='ignore')

    # read the header
    header = []  # a list to store header
    temp_line = ''
    while 'Kurve' not in temp_line:
        temp_line = f.readline()
        header.append(temp_line)  # add header's info into the list
    header = header[:-1]  # remove last item in the header

    curve = []  # a list to hold data of the curve
    curves_df = pd.DataFrame()  # dataframe of all the curves
    curve_nr = 0

    for line in f:  # read all the lines in file
        if 'Kurve' not in line:
            try:
                number = float(line)
                curve.append(number)
            except ValueError:
                pass

        else:  # the 'Kurve' is there, the last curve should end
            curve_nr += 1
            header_nr = 'Kurve_%i' % curve_nr  # create the header

            # save curve in dataframe
            temp_df = pd.DataFrame(curve, columns=[header_nr])
            # join the temp_df to the final dataframe, side by side
            curves_df = pd.concat([curves_df, temp_df], axis=1)

            curve.clear()  # empty the curve

    f.close()  # close the file

    # plot out the last curve
    curve_nr += 1

    # save the last curve in dataframe
    header_nr = 'Kurve_%i' % curve_nr  # create the header
    # save curve in dataframe
    temp_df = pd.DataFrame(curve, columns=[header_nr])
    # join the temp_df to the final dataframe, side by side
    curves_df = pd.concat([curves_df, temp_df], axis=1)

    curve.clear()  # empty the curve

    print(curves_df.describe())

    # save dataframe in new file
    saveData(work_file, curves_df, header)


if __name__ == "__main__":
    main(sys.argv[1:])

