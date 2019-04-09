# -*- coding: utf-8 -*-
"""

File Name      : all_ids.py
Author         : CMMC
Date Created   : ~/2019 
Date Modified  : ~/2019
Python Version : 3.6

"""
# Modules and Libraries 
import os  
import re 


if os.path.exists("C:\\~"):
    path_econproj = r'C:\Users\~Proyectos Economia'
    os.chdir(path_econproj + r'~Soccer Statistics Project')
    path = os.getcwd()
    print("\nCurrent Working Directory is now: ", path)
    
else:
    path_econproj = r'C:\Users\~Proyectos Economia'
    os.chdir(path_econproj + r'~Soccer Statistics Project')
    path = os.getcwd()
    print("\nCurrent Working Directory is now: ", path)

py_path = path + r'\python files'

# 1. List years  
years_ne = ['03','04','05','06','07']
years_we = ['08','09','10','11','12','13','14','15','16','17','18']

# 2. Function 
def get_ids():
    """ get_ids() will return a list with all peruvian matches ids from 2003-2018 that finds as a 
        excel file name in path + r'torneo\str(y)'. These ids consist of all soccer matches during 
        the length of the time that we examine """ 
        
    all_urls = []
    # URL's list of years with no events 
    for y in years_ne: 
        os.chdir(path + r'\torneo'+str(y))
        all_urls.append(os.listdir(os.getcwd()))
        
    # URL's list of years with events  
    for y in years_we:
        os.chdir(path + r'\torneo'+str(y))
        all_urls.append(os.listdir(os.getcwd()))
        
    all_urls = [z      for y in all_urls for z in y]
    all_urls = [re.findall(r'[0-9]+',x)  for x in all_urls]
    all_urls = [str(y) for x in all_urls for y in x]
    
    return all_urls 
    
if __name__ == '__main__':
    get_ids()