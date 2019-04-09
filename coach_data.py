# -*- coding: utf-8 -*-
"""

File Name      : coach_data.py
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
    
    coaches = {}
    try:
        coach_home_xp = driver.find_element_by_xpath("//div[@class='lineups']//div[@class='team team-a']//div[@class='team-coach ']//span[@class='coach']//span[@class='name']")
        coaches['coach_home_name'] = coach_home_xp.text
        
        coach_away_xp = driver.find_element_by_xpath("//div[@class='lineups']//div[@class='team team-b']//div[@class='team-coach ']//span[@class='coach']//span[@class='name']")
        coaches['coach_away_name'] = coach_away_xp.text
    
    except NoSuchElementException as e:
        coaches['coach_home_name'] = None
        coaches['coach_away_name'] = None 
        
    driver.quit() 
    
    ellapsed = time.time() - start_time
    print('%.4f' % ellapsed)    
    
    final_data = {**data, **coaches}
    locals()['data_frame_'+str(id_match)] = pd.DataFrame({k: [v] for k,v in final_data.items()})
    df_list.append(locals()['data_frame_'+str(id_match)])

# 3. CREATE DATABASE   
df = pd.concat(df_list, axis=0, ignore_index=True, sort=False)

df.to_excel(path_econproj + r"~coaches_data.xlsx", header=True, index=False)
