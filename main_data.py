# -*- coding: utf-8 -*-
"""

File Name      : main_data.py
Author         : CMMC
Date Created   : ~/2019
Date Modified  : ~/2019
Python Version : 3.6

"""
# Modules and Libraries
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from get_ids import get_ids
import pandas as pd 
import numpy as np 

from urllib.parse import parse_qs
import os 
import time
 

# 1. SETTING DIR 
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

all_urls         = get_ids()
not_scraped_urls = []
df_list          = []

# 2. LOOP
for id_match in all_urls:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')        
    options.add_argument('--incognito')
    prefs = {'profile.managed_default_content_setting.images':2, 'disk-cache-size': 4096}
    
    driver = webdriver.Chrome(executable_path = py_path + '\chromedriver.exe', options=options)
    driver.delete_all_cookies()
    
    url    = r'http://www.soccerway.mobi/?sport=soccer&page=match&id='+str(id_match)+'&_teamtype=default&localization_id=www' 
    driver.implicitly_wait(5)
    
    driver.get(url)
    start_time = time.time()
    driver.implicitly_wait(1)
    
    timeout = 20
    
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located((By.XPATH,"//div[@class='clearfix subnav level-1']//li[2]//a")))
        print("Succesfully visibility for id_match: ", id_match)
    except TimeoutException:
        print("Timed out waiting for id_match: "     , id_match)
        not_scraped_urls.append(id_match)
        continue 
    
    data = {}
    data['match_id'] = parse_qs(driver.find_element_by_xpath("//div[@class='clearfix subnav level-1']//li[2]//a[3]").get_attribute('href'))['id'][0]
    data['area_id']        = parse_qs(driver.find_element_by_xpath("//div[@class='clearfix subnav level-1']//li[2]//a[1]").get_attribute('href'))['area_id'][0]
    data['competition_id'] = parse_qs(driver.find_element_by_xpath("//div[@class='clearfix subnav level-1']//li[2]//a[2]").get_attribute('href'))['id'][0]
    
    data['area']           = driver.find_element_by_xpath("//div[@class='clearfix subnav level-1']//li[2]//a[1]").text
    data['competition']    = driver.find_element_by_xpath("//div[@class='clearfix subnav level-1']//li[2]//a[2]").text 
    
    data['home_team']      = driver.find_element_by_xpath("//div[@class='container left']//h3//a").text
    data['away_team']      = driver.find_element_by_xpath("//div[@class='container right']//h3//a").text
    
    middle_elements = driver.find_elements_by_xpath("//div[@class='details clearfix']")
    
    for elem in middle_elements:
        data['date']          = elem.find_element_by_xpath("//dl//dt[.='Date']/following-sibling::dd").text
        try:
            data['game_week']     = elem.find_element_by_xpath("//dl//dt[.='Game Week']/following-sibling::dd").text
        except NoSuchElementException as e:
            data['game_week']     = np.NaN
            
        try:
            data['kick_off']      = elem.find_element_by_xpath("//dl//dt[.='Kick-off']/following-sibling::dd").text            
        except NoSuchElementException as e:
            data['kick_off']      = np.NaN
          
        try:
            data['half_time']     = elem.find_element_by_xpath("//dl//dt[.='Half-time']/following-sibling::dd").text
        except NoSuchElementException as e:
            data['half_time']     = np.NaN
    
        data['full_time']     = elem.find_element_by_xpath("//dl//dt[.='Full-time']/following-sibling::dd").text
        
        try:
            data['extra_time']    = elem.find_element_by_xpath("//dl//dt[.='Extra-time']/following-sibling::dd").text
        except NoSuchElementException as e:
            data['extra_time']    = np.NaN 
            
        try:
            data['penalties']     = elem.find_element_by_xpath("//dl//dt[.='Penalties']/following-sibling::dd").text
        except NoSuchElementException as e:
            data['penalties']     = np.NaN
    
        try:
            data['aggregate']     = elem.find_element_by_xpath("//dl//dt[.='On aggregate']/following-sibling::dd").text
        except NoSuchElementException as e:
            data['aggregate']     = np.NaN 
        
        try:
            data['venue']         = elem.find_element_by_xpath("//dl//dt[.='Venue']/following-sibling::dd").text
        except NoSuchElementException as e:
            data['venue']         = np.NaN
        
        try:
            data['attendance']    = elem.find_element_by_xpath("//dl//dt[.='Attendance']/following-sibling::dd").text
        except NoSuchElementException as e:
            data['attendance']    = np.NaN  

    
    driver.quit() 
    
    ellapsed = time.time() - start_time
    print('%.4f' % ellapsed)    
    
    final_data = {**data}
    locals()['data_frame_'+str(id_match)] = pd.DataFrame({k: [v] for k,v in final_data.items()})
    df_list.append(locals()['data_frame_'+str(id_match)])

# 3. CONCATENATE AND CREATE DATABASE
df = pd.concat(df_list, axis=0, ignore_index=True, sort=False)

df.to_excel(path_econproj + r"\~main_data.xlsx", header=True, index=False)