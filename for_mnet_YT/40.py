#-*- coding: utf-8 -*-
import requests
import pandas as pd
import openpyxl
from pandas import DataFrame
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from tqdm import tqdm
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

***********************
'''
StratPoint = 2955 #<----여기에 숫자 넣어주시면 되용!
EndPoint = 2957

fail_list = []
fail_list_title = []
title_list = []
Success_list = []

# chrome_options.add_argument('--headless')
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") 
driver = webdriver.Chrome(ChromeDriverManager().install(),
    chrome_options=options)

def rtYTURL(watch, pk):
    URL = 'https://www.youtube.com'
    return SecondCraw(URL + watch, pk)

def SecondCraw(URL, pk):
    CONTENT = []
    driver.get(URL)
    html = driver.page_source
    s = bs(html, 'html.parser')

    #mv_title
    SectorA = s.select('#container > h1 > yt-formatted-string')

    #mv_view
    SectorB = driver.find_elements_by_css_selector('#count > yt-view-count-renderer > span.view-count.style-scope.yt-view-count-renderer')

    #mv_register
    # SectorC = driver.find_elements_by_css_selector('#owner-name > a')

    #mv_regist_date
    SectorD = driver.find_elements_by_css_selector('#upload-info > span')

    #현재 pk는 singer_list의 pk가 아닌 mnet의 pk
    data={"series_id":pk,"cd_date":SectorD, 'Cd_content': SectorA, 'cd_url':URL, 'cd_view':SectorB}
    CONTENT.append(data)
    return CONTENT

def Searching(mnet_cd_idx ,page_num):
    # print(mnet_cd_idx)
    if (mnet_cd_idx == 2) : 
        data = {'cd_idx':mnet_cd_idx,'mv_name':'2', 'query':name + ' ' + '2', 'regist_date': '2', 'pk':pk}
        title_list.append(data)
        fail_list.append(data)
    for page in range(int(page_num)):
        try :
            driver.get(f'http://www.mnet.com/artist/{mnet_cd_idx}/vods?gcode=1&otype={page}')
            soup = bs(driver.page_source, 'html.parser')
            regist = soup.select('#content > div.link_movie.border_0.mb0 > div > ul > li > dl')
            if (len(regist)==0):
                data = {'cd_idx':mnet_cd_idx,'mv_name':'2', 'query':name + ' ' + '2', 'regist_date': '2', 'pk':pk}
                title_list.append(data)
            for titles in regist:
                try :
                    # 각각의 영상 타이틀 제목의 tag 제거
                    tag_title_name = titles.select('dt > a')
                    title_name = tag_title_name[0].text
                
                    # 각각의 영상 등록일 
                    date=re.findall("[0-9]{4}.[0-9]{2}.[0-9]{2}",str(titles))

                    if '티저' in title_name :
                        continue
                    else : 
                        data = {'cd_idx':mnet_cd_idx,'mv_name':title_name, 'query':name + ' ' + title_name, 'regist_date': date, 'pk':pk}
                        title_list.append(data)
                        Success_list.append(data)
                except :
                    data = {'cd_idx':mnet_cd_idx,'mv_name':title_name, 'query':name + ' ' + title_name, 'regist_date': date, 'pk':pk}
                    fail_list_title.append(data)
                    continue     
        except :
            data = {'cd_idx':mnet_cd_idx, 'name':name}
            fail_list.append(data)
            continue

def Is_it_be(mnet_cd_idx):
    try :  
        driver.get(f'http://www.mnet.com/artist/{mnet_cd_idx}/vods?gcode=1')
        soup = bs(driver.page_source, 'html.parser', from_encoding='utf-8')
        page_num = soup.select_one('#content > div.paging_type_no > a:last-child').get_text()
        return(page_num)
    except :
        page_num = 1
        return(page_num)

def save_fail_list(fail_list, fail_title_list):
    result_df=pd.DataFrame(fail_list,columns=['cd_idx','name'])
    result_df=pd.DataFrame(fail_list_title,column=['cd_idx','mv_name', 'query', 'regist_date', 'pk'])
    result_df.to_excel(f'~/Desktop/mycelebs/WebCrawling/190712/fail_star_result_mnet_star_id_190709.xlsx',index=False)
    result_df.to_excel(f'~/Desktop/mycelebs/WebCrawling/190712/fail_list_result_mnet_star_id_190709.xlsx',index=False)
def Save_Excel(Success_list, title_list, fail_list):
    result_df_Success=pd.DataFrame(Success_list,columns=['cd_idx','mv_name', 'query', 'regist_date', 'pk'])
    result_df_All=pd.DataFrame(title_list,columns=['cd_idx','mv_name', 'query', 'regist_date', 'pk'])
    result_df_Fail=pd.DataFrame(fail_list,columns=['cd_idx','mv_name', 'query', 'regist_date', 'pk'])
    result_df_Success.to_excel(f'~/Desktop/mycelebs/WebCrawling/190712/40Success_result_mnet_star_id_190709.xlsx',index=False)
    result_df_All.to_excel(f'~/Desktop/mycelebs/WebCrawling/190712/40result_mnet_star_id_190709.xlsx',index=False)
    result_df_Fail.to_excel(f'~/Desktop/mycelebs/WebCrawling/190712/40fail_result_mnet_star_id_190709.xlsx',index=False)    


if __name__ == '__main__':

    df = pd.read_excel("~/Desktop/mycelebs/WebCrawling/190712/singer_list.xlsx")
    name = df['name']
    pk = df['pk']
    mnet_cd_idx = 194934


    # print('아티스트 : ' + name +':'+ str(paged))
    Searching(194934, 1)
    Save_Excel(Success_list, title_list, fail_list)
    cprint('\n Complete Success \n', 'red')        
        


    