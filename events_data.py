# -*- coding: utf-8 -*-
"""

File Name      : events_data.py
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

    try:
        events_home = driver.find_elements_by_xpath("//div[@class='lineups']//div[@class='team team-a']//ul[@class='players']//span[@class='events']//span[@class='event']")
        home_events = {}
        for idx, event in enumerate(events_home):
            title     = event.find_element_by_xpath('.//span').get_attribute('title')
            min_event = event.find_element_by_xpath(".//span[@class='minute']").text.strip("'")
            
            home_events['event_name_'+ str(idx+1) + '_h'] = str(title.strip())
            home_events['event_min_' + str(idx+1) + '_h'] = min_event
            
    except NoSuchElementException as e:
        pass 

    try:
        events_away = driver.find_elements_by_xpath("//div[@class='lineups']//div[@class='team team-b']//ul[@class='players']//span[@class='events']//span[@class='event']")
        away_events = {}
        
        for idx, event in enumerate(events_away):
            title     = event.find_element_by_xpath('.//span').get_attribute('title')
            min_event = event.find_element_by_xpath(".//span[@class='minute']").text.strip("'")
            
            away_events['event_name_'+ str(idx+1) + '_a'] = str(title.strip())
            away_events['event_min_' + str(idx+1) + '_a'] = min_event
    except NoSuchElementException as e:
        pass 
    
    try:
        events_home_substitutes = driver.find_elements_by_xpath("//div[@class='substitutes']//div[@class='team team-a']//ul[@class='players']//span[@class='events']//span[@class='event']")
        home_events_substitutes = {}
        
        for idx, event in enumerate(events_home_substitutes):
            title     = event.find_element_by_xpath('.//span').get_attribute('title')
            min_event = event.find_element_by_xpath(".//span[@class='minute']").text.strip("'")
            
            home_events_substitutes['event_name_'+ str(idx+1) + '_hs'] = str(title.strip())
            home_events_substitutes['event_min_' + str(idx+1) + '_hs'] = min_event
    except NoSuchElementException as e:
        pass 
    
    try:    
        events_away_substitutes = driver.find_elements_by_xpath("//div[@class='substitutes']//div[@class='team team-b']//ul[@class='players']//span[@class='events']//span[@class='event']")
        away_events_substitutes = {}
        
        for idx, event in enumerate(events_away_substitutes):
            title     = event.find_element_by_xpath('.//span').get_attribute('title')
            min_event = event.find_element_by_xpath(".//span[@class='minute']").text.strip("'")
            
            away_events_substitutes['event_name_'+ str(idx+1) + '_as'] = str(title.strip())
            away_events_substitutes['event_min_' + str(idx+1) + '_as'] = min_event
    except NoSuchElementException as e:
        pass 
    
    driver.quit() 
    
    ellapsed = time.time() - start_time
    print('%.4f' % ellapsed)    
    
    final_data = {**data, **home_events, **away_events, **home_events_substitutes, **away_events_substitutes}
    locals()['data_frame_'+str(id_match)] = pd.DataFrame({k: [v] for k,v in final_data.items()})
    df_list.append(locals()['data_frame_'+str(id_match)])

# 3. CREATE DATABASE  
df = pd.concat(df_list, axis=0, ignore_index=True, sort=False)

df.to_excel(path_econproj + r"~events_data.xlsx", header=True, index=False)

    