import sys, getopt
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
    Save data of the curve in to th temp file

    Input:
        file_name (str): name of the temp file
        curve_nr (int): number of the curve
        curve (list): data
        header (list): measurement infomation
'''
def save_data(file_name, curve_nr, curve, header):
    # create a tmp folder to hold the files
    if not os.path.isdir('tmp'):
        print('tmp folder not found. Create it\n')
        os.mkdir('tmp')

    # build the path
    file_name = './tmp/' + file_name

    f = open(file_name, 'a') # create tmp file to hold data

    # write the header before the 1st curve
    if curve_nr == 1:
        for data in header:
            f.write("%s\n" % data)

    f.write("\n")
    f.write("Kurve %i\n\n" % curve_nr)

    # write the data of the curve
    for data in curve:
        f.write("%s\n" % data)

    f.close() # close the file

'''
    Save the image of the saved plot into img folder

    Input:
        file_name (str): name of working file
        curve_nr (int): number of the curve
'''
def save_image(file_name, curve_nr):
    # create a tmp folder to hold the files
    if not os.path.isdir('tmp/img'):
        print('tmp/img folder not found. Create it\n')
        os.mkdir('tmp/img')

    tmp = "_" + str(curve_nr) + ".png" # enumerate the curve and and png extension
    file_name = file_name.replace(".txt", tmp) # change the extension to png
    file_name = './tmp/img/' + file_name # build the path
    plt.savefig(file_name, bbox_inches='tight')

'''
    Get the information of the test from the header

    Input:
        header (list): header
    Output
        (str) Infomation of the test

'''
def get_info(header):
    info = ''
    temp = []
    for line in header:
        if 'Info' in line: # found the info line
            # extract the information
            temp = line.split(":") # split string with :
            info = temp[1].strip() # remove the white space aroung it

    return info

def main(argv):
    # get the commandline options
    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "input="])
    except getopt.GetoptError:
        print('read_files.py -i <inputfile>')
        sys.exit(2)

    # parse the options and arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('read_files.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            work_file = arg # name of working file

    f = open(work_file, 'r', encoding='utf-8', errors='ignore') # open to read working file

    header = [] # a list to hold the info in header

    # read the header
    temp_line = ''
    while 'Kurve' not in temp_line:
        temp_line = f.readline()
        header.append(temp_line) # add header's info into the list
        print(temp_line)
    header = header[:-2] # remove two last item in the header

    info = get_info(header) # this should be title of the plot

    curve = [] # a list to hold data of the curve
    curve_nr = 0

    # setup the plot
    plt.close('all') # close all the previous figures
    plt.figure()
    plt.show(block=False) # show the plot but non blocking


    '''
    begin to read measurement data
    '''
    for line in f:
        if 'Kurve' not in line:
            # parse data of the curve in list
            try:
                number = float(line)
                curve.append(number)
            except ValueError:
                pass

        else:
            # the 'Kurve' is there, the last curve should end
            plt.clf() # clear figure
            plt.title(info)
            plt.plot(curve) # plot the curve
            plt.xlim(0,2500) # limit x axis from 0 to 2500
            plt.ylim(0,0.22) # limit y axis from 0 to 0.22
            plt.draw() # draw the curve on the open figure

            # ask user to keep or delete the data
            user_input = ''
            while user_input not in ('y', 'n', 'q'):
                user_input = input('Quit (q) or keep the curve (y/n)?: ')

            if user_input == 'y':
                print('keep')
                curve_nr += 1
                save_data(work_file, curve_nr, curve, header)
                save_image(work_file, curve_nr)
                curve.clear() # empty the curve
            elif user_input == 'n':
                print('delete')
                curve.clear() # empty the curve
            else:
                print('I am quit')
                f.close() # close the working file
                sys.exit(2)

    '''
    plot out the last curve
    '''
    plt.clf() # clear figure
    plt.title(info)
    plt.plot(curve) # plot the curve
    plt.xlim(0,2500) # limit x axis from 0 to 2500
    plt.ylim(0,0.22) # limit y axis from 0 to 0.22
    plt.draw() # draw the curve on the open figure

    # ask user to keep or delete the data
    user_input = ''
    while user_input not in ('y', 'n', 'q'):
        user_input = input('Quit (q) or keep the curve (y/n)?: ')

    if user_input == 'y':
        print('keep')
        curve_nr += 1
        save_data(work_file, curve_nr, curve, header)
        save_image(work_file, curve_nr)
        curve.clear() # empty the curve
    elif user_input == 'n':
        print('delete')
        curve.clear() # empty the curve
    else:
        print('I am quit')
        f.close() # close the working file
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])


