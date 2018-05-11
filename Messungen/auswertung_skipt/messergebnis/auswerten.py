# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys

def get_header(file_path):
    """ Get the header form the measurement file

        Input:
            file_path (str): path to measurement file
        Output
            header (list): header of the measurement file

    """
    f = open(file_path, 'r', encoding='utf-8', errors='ignore') # open to read working file

    header = [] # a list to store header
    temp_line = ''
    while 'Kurve' not in temp_line:
        temp_line = f.readline()
        header.append(temp_line) # add header's info into the list
        
    header = header[:-2] # remove two last item in the header

    f.close() # close the file
    
    return header

def get_info(header):
    """ Get the information of the test from the header

        Input:
            header (list): header
        Output
            (str) Infomation of the test

    """

    info = '' # empty string to store info of the measurement
    temp = [] # empty list to store the splited string
    for line in header:
        if 'Info' in line: # found the info line
            temp = line.split(":") # split string with ':'
            info = temp[1].strip() # get the info and remove the white space around it

    return info

def parse_info(info_str):
    """ Parse the information from the test and extract the test parameters
        
        Input:
            info_str (str): a long param information and should be in this format:
                            'FVA3, v = 1.47, T = 80, F = 20, h = 214.9'
            
        Output:
            param (tuple): value of the test parameters
    """
    info_splited = info_str.split(',') # split the info with ','
    
    # remove the white space of item in list
    info_splited = [x.strip() for x in info_splited]
    
    oil = info_splited[0] # oil
    
    params = () # oil speed temperature load thickness
    params += (oil, ) # add oil in to the params tuple
    
    # add another parameter in to the params tuple
    for param_str in info_splited[1:]:
        value = get_param(param_str)
        params += (value, )
        
    return params

def get_param(param_str):
    """ Extract the parameter's value from it's long string
        
        Input:
            param_str (str): a long parameter string in this format 'para = 1.23'
            
        Output:
            param (float): value of the parameter
    """
    param = param_str.split('=')
    try:
        param = float(param[1].strip()) # convert the value from str to float
    except ValueError:
        param = 0 # return 0 if there is error during convertion str to float
    
    return param

def plot_c_h_v(data_frame):
    # plot capacitance and film over the speed
    speeds = data_frame['Speed']
    capacitances = data_frame['Kap_10_F']
    films = data_frame['Film']
    
    fig, ax1 = plt.subplots()
    ax1.plot(speeds, capacitances, 'g^')
    ax1.set_xlabel('Speed')
    ax1.set_ylabel('Cap')
    
    ax2 =ax1.twinx()
    ax2.plot(speeds, films, 'ro')
    ax2.set_ylabel('Film')
    
    fig.tight_layout()

results_file = 'messergebnisse.txt'
# FileName	Kap_1_F	Kap_2_F	Kap_3_F	Kap_4_F	Kap_5_F	Kap_6_F	Kap_7_F	Kap_8_F	Kap_9_F	Kap_10_F

results = pd.read_csv(results_file, sep='\t') # read the results in panda dataframe

# a data frame to hold the parameters form the test
params_df = pd.DataFrame(columns = ['Oil', 'Speed', 'Temperature', 'Load', 'Film'])

# reading information from the test
for file_name in results['FileName']:
    # build the file path
    file_path = './input/' + file_name + '.txt'
    
    # check if file exits
    if os.path.isfile(file_path):
        header = get_header(file_path) # get header of the measurement
        info = get_info(header) # get infomation of the test
        params = parse_info(info) # get all the test parameters
        params_df.loc[len(params_df)] = list(params) # save the thes parameters
        
# add the test paramters in to results dataframe
results = pd.concat([results, params_df], axis=1, join_axes=[results.index])

# get the result for test at 40, 60 and 80 C and save it
results_40 = results.loc[results['Temperature'] == 40 ]
results_60 = results.loc[results['Temperature'] == 60 ]
results_80 = results.loc[results['Temperature'] == 80 ]

# remove the coulums with all zeros in it and nan
results_40 = results_40.loc[:, (results_40 != 0).any(axis=0)].dropna()
results_60 = results_60.loc[:, (results_60 != 0).any(axis=0)].dropna()
results_80 = results_80.loc[:, (results_80 != 0).any(axis=0)].dropna()

results_40_FVA3_20N = results_40.loc[(results_40['Oil'] == 'FVA3') &
                                     (results_40['Load'] == 20)]
results_40_FVA3_10N = results_40.loc[(results_40['Oil'] == 'FVA3') & 
                                     (results_40['Load'] == 10)]
results_40_SHC = results_40.loc[results_40['Oil'] == 'SHC320']


# save result in to csv
#results_40_FVA3_20N.to_csv('results_40C_FVA3_20N.csv')
#results_40_FVA3_10N.to_csv('results_40C_FVA3_10N.csv')
#results_40_SHC.to_csv('results_40C_SHC.csv')
#results_60.to_csv('results_60C.csv')
#results_80.to_csv('results_80C.csv')