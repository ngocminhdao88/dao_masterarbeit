# -*- coding: utf-8 -*-
info = 'FVA3, v = 1.47, T = 80, F = 20, h = 214.9'

def get_param(param_str):
    """ Extract the parameter's value from it's long string
        
        Input:
            param_str (str): a long parameter string in this format 'para = 1.23'
            
        Output:
            param (float): value of the parameter
    """
    param = param_str.split('=')
    param = float(param[1].strip())
    
    return param

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