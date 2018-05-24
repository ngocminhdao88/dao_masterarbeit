import sys
import getopt
import os
import matplotlib.pyplot as plt
"""
Reformat the measuremnt film from the software ST Meter Plus
"""


def usage():
    """
    Print out the help how to use this file
    """
    print(__doc__)


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

    # open working file
    f = open(work_file, 'r')

    header = f.readline()
    time_hd = header[0]
    cp_hd = header[1]

    time_ls = []
    cp_ls = []

    # read the data from the file
    for line in f:
        datas = line.split(',')

        time_data = datas[0].split(' ')
        time = time_data[0].strip()
        time_ls.append(int(time))  # convert time from str to int
        time_unit = time_data[1].strip()

        cp_data = datas[1].split(' ')
        cp = cp_data[0].strip()
        cp_ls.append(float(cp))  # convert cp from str to float
        cp_unit = cp_data[1].strip()

    # close the film when done with it
    f.close()

    # create a folder to store all the images
    if not os.path.isdir("imgs"):
        print("imgs not found. Create it\n")
        os.mkdir("imgs")

    # setup the plot
    fig, ax = plt.subplots()
    ax.plot(time_ls, cp_ls)
    ax.set_xlabel("Time [%s]" % time_unit)
    ax.set_ylabel("Cp [%s]" % cp_unit)
    ax.set_title(work_file)

    # save the figure
    img_path = "./imgs/" + work_file + ".png"
    fig.savefig(img_path, bbox_inches="tight")

if __name__ == "__main__":
    main(sys.argv[1:])
