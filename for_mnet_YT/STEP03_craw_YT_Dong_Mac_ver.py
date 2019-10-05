#-*- coding: utf-8 -*-
from youtube_dl import YoutubeDL
import requests
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import openpyxl
from tqdm import tqdm; tqdm.pandas(desc="working")
import time
import numpy as np
import ast
import re
from webdriver_manager.chrome import ChromeDriverManager
from termcolor import cprint, colored



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
***********************
에러 나서 멈췃을 시, 터미널 하단의 
OOit << start + OO숫자 넣어서 
StartPoint 변수값에 넣어서 다시 돌려주시면 되용!
정말 캄삼다!
'''
StratPoint = 49 #<----여기에 숫자 넣어주시면 되용!
EndPoint = 149

fail_list = []
fail_list_title = []
title_list = []
Success_list = []

# chrome_options.add_argument('--headless')
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") 
driver = webdriver.Chrome(ChromeDriverManager().install(),
    chrome_options=options)

# def rtYTURL(watch, pk):
#     URL = 'https://www.youtube.com'
#     return str(URL + watch)

def SecondCraw(URL, pk):
    driver.get(URL)
    # html = driver.page_source
    # s = bs(html, 'html.parser')

    #mv_title
    try:
        time.sleep(1)
        SectorA = driver.find_elements_by_xpath('//*[@id="container"]/h1/yt-formatted-string')[0].text
    except:
        SectorA=np.nan

    #mv_view
    try:
        SectorB = driver.find_elements_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]')[0].text
    except:
        SectorB=np.nan

    #mv_register
    try:
        SectorC = driver.find_elements_by_xpath('//*[@id="owner-name"]/a')[0].text
    except:
        SectorC=np.nan
    #mv_regist_date
    try:
        SectorD = driver.find_elements_by_xpath('//*[@id="upload-info"]/span')[0].text 
    except:
        SectorD=np.nan
    #inspecting
    # print(SectorA + '\n SectorA \n' + SectorB + '\n SectorB \n' + SectorC + '\n SectorC \n' + SectorD + '\n SectorD \n ')[0].text

    #현재 pk는 singer_list의 pk가 아닌 mnet의 pk
    data={"series_id":pk,"cd_date":SectorD, 'cd_content': SectorA, 'cd_url':URL, 'cd_channel':SectorC, 'cd_view':SectorB}
    title_list.append(data)
    Success_list.append(data)

def Searching(query):
    query2 = []
    query2 = query.split(' ')
    name = query2[0]
    query2.pop(0)
    song = ' '.join(query2)
    driver.get(f"https://www.youtube.com/results?search_query={name}+\"{song}\"+ \"MV\"")
    Vdeo = driver.find_element_by_css_selector("a#video-title")
    Vdeo_url = Vdeo.get_attribute("href")
    return Vdeo_url

def Save_Excel(Success_list, title_list, fail_list):
    result_df_Success=pd.DataFrame(Success_list,columns=['series_id','cd_date', 'cd_content', 'cd_url', 'cd_channel', 'cd_view'])
    result_df_All=pd.DataFrame(title_list,columns=['series_id','cd_date', 'cd_content', 'cd_url', 'cd_channel', 'cd_view'])
    result_df_Fail=pd.DataFrame(fail_list,columns=['series_id','cd_date', 'cd_content', 'cd_url', 'cd_channel', 'cd_view'])
    result_df_Success.to_excel(f'/Users/mycelebs_dev/pycharmprojects/web_clowling/190712/Success_result_YT_Mnet_999.xlsx',index=False)
    result_df_All.to_excel(f'/Users/mycelebs_dev/pycharmprojects/web_clowling/190712/result_YT_Mnet_999.xlsx',index=False)
    result_df_Fail.to_excel(f'/Users/mycelebs_dev/pycharmprojects/web_clowling/190712/fail_result_YT_Mnet_999.xlsx',index=False)    


# def get_cations_URL(row):
#     URL = Searching(row['query'])
#     ydl_opts = {
#         'skip_download': True,
#         'nocheckcertificate': True,
#         'ignoreerrors': True,
#         'no_warnings': True,
#         'quiet': True,
#         'writesubtitles': True,
#         'writeautomaticsub': True
#     }
#     #"series_id":pk,"cd_date":SectorD, 'cd_content': SectorA, 'cd_url':URL, 'cd_channel':SectorC, 'cd_view':SectorB
#     cols = ['upload_date', 'title', 'uploader', 'view_count']
#     ydl = YoutubeDL(ydl_opts)
#     res = ydl.extract_info(URL, download=False)
#     row['cd_date'] = res['upload_date']
#     row['cd_content'] = res['title']
#     row['cd_channel'] = res['uploader']
#     row['cd_view'] = res['view_count']
#     row['cd_url'] = URL
#     row['series_id'] = row['pk']
#     return row

# def sav_ex(RESULT_LIST):
#     result_df=pd.DataFrame(RESULT_LIST,columns=['series_id','cd_date', 'cd_content', 'cd_url', 'cd_channel', 'cd_view'])
#     result_df.to_excel(f'/Users/mycelebs_dev/pycharmprojects/web_clowling/190712/Success_result_YT_Mnet_190714.xlsx',index=False)

if __name__ == '__main__':
    df = pd.read_excel("/Users/mycelebs_dev/PycharmProjects/web_clowling/190712/title_result_mnet_star_id_190709.xlsx")
    query = df['query']
    pk = df['pk']
    
    with tqdm(total=(EndPoint-StratPoint)) as pbar:
        for idx,row in tqdm(df[StratPoint:EndPoint].iterrows(), ascii=True, desc="Rolling in the deep - Vazquez Sounds"):
            pk = row['pk']
            query = row['query']
            mv_name = row['mv_name']
            if mv_name == '2':
                # print('없는 아티스트 :' + name)
                data = {"series_id":pk,"cd_date":' ', 'cd_content': ' ', 'cd_url':' ' , 'cd_channel':' ', 'cd_view':' '}
                title_list.append(data)
                fail_list.append(data)
                continue
            else : 
                # print('아티스트 : ' + name +':'+ str(paged))
                Vdeo_url = Searching(query)
                Complete_url = rtYTURL(Vdeo_url)
                SecondCraw(Vdeo_url, pk)
                # get_cations_URL(Vdeo_url, pk)
            pbar.update()
    Save_Excel(Success_list, title_list, fail_list)
    # sav_ex(RESULT_LIST)
    cprint('\n Complete Success \n', 'red')        
        

    
