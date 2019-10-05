#-*- coding: utf-8 -*-
import requests
import pandas as pd
import openpyxl
from pandas import DataFrame
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
#from __future__ import division, print_function, unicode_literals
import time
import numpy as np
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

'''
======================
총 갯수 23656
======================
지은님 startPoint : 0 
      EndPoint : 4000
채원님 startPoint : 4001 
      EndPoint : 8000
보솔님 startPoint : 8001 
      EndPoint : 12000
하영님 startPoint : 12001
      EndPoint : 16000
동수님 startPoint : 16001 
      EndPoint : 20000
extra startPoint : 20001 
      EndPoint : 23656
***********************
에러 나서 멈췃을 시, 터미널 하단의 
OOit << start + OO숫자 넣어서 
StartPoint 변수값에 넣어서 다시 돌려주시면 되용!
'''
StartPoint =  20001 #<----여기에 숫자 넣어주시면 되용!
EndPoint =   23656 #<----여기에 숫자 넣어주시면 되용!

DriverPath = '/Users/mycelebs_dev/PycharmProjects/web_clowling/190704/chromedriver' #<----여기에 경로 넣어주심 되용!!
ResourceExcelPath = '/Users/mycelebs_dev/PycharmProjects/web_clowling/190704/coo_data_190704.xlsx' #<----여기에 경로 넣어주심 되용!!

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(executable_path='/Users/mycelebs_dev/PycharmProjects/web_clowling/chromedriver/chromedriver',
#     chrome_options=chrome_options)
# df = pd.read_excel("/Users/mycelebs_dev/PycharmProjects/web_clowling/190704/coo_data_190704.xlsx")
# cd_idx = df['cd_name']
driver = webdriver.Chrome(executable_path=DriverPath,
    chrome_options=chrome_options)
df = pd.read_excel(ResourceExcelPath)
cd_idx = df['cd_name']


result_df = df.loc[:, ['cd_name']] # DataFrame(data = {"food_name" : [], "food_url" : []}) # df.loc[:, ['cd_name']]
rdf_i = 0

data_list=[]
for idx,row in tqdm(df[StartPoint:EndPoint].iterrows(),desc="돌리는중"):
    cd_name=row['cd_name']
    try:
        youtubeUrl=(f"https://www.youtube.com/results?search_query={cd_name}+만들기+-먹방")
        driver.get(youtubeUrl)
        url_list = []

        box_list = driver.find_elements_by_css_selector("a#video-title")
        # print(box_list)
        num=0
        for box in box_list:
            try:
                url=box.get_attribute("href")
                num+=1
                # print(url)
            except:
                continue
            url_list.append(url)
            if(num==6):
                food_make_url = "\n".join(url_list)
                # print(food_make_url)
                data={"cd_name":cd_name,"food_make_url":food_make_url}
                data_list.append(data)
                break

    except:
        print(idx)
        result_df=pd.DataFrame(data_list,columns=['cd_name','food_make_url'])
        result_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190704/result_coo_data_{idx}_190704.xlsx',index=False)
        driver.close()


result_df=pd.DataFrame(data_list,columns=['cd_name','food_make_url'])
result_df.to_excel('/Users/mycelebs_dev/PycharmProjects/web_clowling/190704/result_coo_data_190704.xlsx',index=False)
driver.close()


# for name in tqdm(result_df['cd_name']):
#     try:
#     youtubeUrl=(f"https://www.youtube.com/results?search_query={name}+만들기")
#     driver.get(youtubeUrl)

#     box_list = driver.find_elements_by_css_selector("a#video-title")
#     print(box_list)


#     num=0
#     for box in box_list:
#         try:
#             url=box.get_attribute("href")
#             num+=1
#             print(url)
#         except:
#             continue
#         url_list.append(url)
#         if(num==6):
#             break

#     food_make_url = ",".join(url_list)
#     print(food_make_url)
#     query=f'{name}+만들기'
#     # result_df.loc[rdf_i] = ['cd_name']
#     rdf_i += 1

#     time.sleep(2)


# # writer = pd.ExcelWriter('/Users/mycelebs_15/Desktop/celebs/ad_result.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
# result_df=pd.DataFrame(url_list)
# result_df.to_excel('/Users/mycelebs_dev/PycharmProjects/web_clowling/190704/result_coo_data_190704.xlsx',index=False)

# driver.close()
