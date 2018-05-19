# -*- coding: utf-8 -*-
"""
Remove all the blank line in file
"""

import sys, getopt, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def usage():
    print(__doc__)

def main(argv):
    """
    """
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
            sys.exit()
        elif opt in ("-i" , "--input"):
            work_file = arg # name of working file
        else:
            assert False, "wrong option"
     
    if not os.path.isdir('no_blank_lines'):
        print('folder not found. Create it\n')
        os.mkdir('no_blank_lines')

    # build the path
    file_name = './no_blank_lines/' + work_file
    # open to read working file            
    f = open(work_file, 'r', encoding='utf-8', errors='ignore')
    temp_file = open(file_name, 'w', encoding='utf-8', errors='ignore')

    for line in f:
        if len(line) > 1:
            temp_file.write(line)
            #print(line)
    f.close()
    temp_file.close()
            
if __name__ == "__main__":
    main(sys.argv[1:])