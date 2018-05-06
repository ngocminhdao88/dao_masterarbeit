import sys, getopt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main(argv):

    # get the commandline options
    try:
        opts, args = getopt.getopt(argv, "hi:", ["help", "input="])
    except getopt.GetoptError:
        print('auswertung.py -i <inputfile>')
        sys.exit(2)

    # parse the options and arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('auswertung.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            work_file = arg # name of working file

    f = open(work_file, 'r', encoding='utf-8', errors='ignore') # open to read working file

    # read the header
    temp_line = ''
    while 'Kurve' not in temp_line:
        temp_line = f.readline()
        print(temp_line)

    curve = []
    counter = 0

    for line in f: # read all the lines in file
        if 'Kurve' not in line:
            try:
                number = float(line)
                curve.append(number)
            except ValueError:
                pass

        else: # the 'Kurve' is there, the last curve should end
            counter += 1
            plt.figure(counter)
            plt.xlim(0,2500)
            plt.ylim(0,0.22)
            plt.plot(curve)
            plt.draw()

            curve.clear() # empty the curve

    # plot out the last curve
    counter += 1
    plt.figure(counter)
    plt.xlim(0,2500)
    plt.ylim(0,0.22)
    plt.plot(curve)
    plt.draw()

    curve.clear() # empty the curve

    f.close() # close the file

    plt.show(block=False)

if __name__ == "__main__":
    main(sys.argv[1:])

