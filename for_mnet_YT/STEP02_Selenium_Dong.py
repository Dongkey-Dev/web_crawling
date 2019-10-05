#-*- coding: utf-8 -*-
import requests
import pandas as pd
import openpyxl
from pandas import DataFrame
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from tqdm import tqdm
import time
from termcolor import cprint, colored
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
StratPoint = 2955 #<----여기에 숫자 넣어주시면 되용!
EndPoint = 2957

fail_list = []
Success_list = []
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
            # titles = soup.select('#content > div.link_movie.border_0.mb0 > div > ul > li > dl > dt > a')
            regist = soup.select('#content > div.link_movie.border_0.mb0 > div > ul > li > dl')
            if (regist==[] ) :
                data = {'cd_idx':mnet_cd_idx,'mv_name':'null', 'query':name, 'regist_date':'null', 'pk':pk}
                title_list.append(data)
                fail_list.append(data)
                continue
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
    result_df=pd.DataFrame(fail_list_title,columns=['cd_idx','mv_name', 'query', 'regist_date', 'pk'])
    result_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190712/fail_star_result_mnet_star_id_190709.xlsx',index=False)
    result_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190712/fail_list_result_mnet_star_id_190709.xlsx',index=False)
def Save_Excel(list1, list2, list3):
    list1_df=pd.DataFrame(list1,columns=['cd_idx','mv_name', 'query', 'regist_date', 'pk'])
    list2_df=pd.DataFrame(list2,columns=['cd_idx','mv_name', 'query', 'regist_date', 'pk'])
    list3_df=pd.DataFrame(list3,columns=['cd_idx','mv_name', 'query', 'regist_date', 'pk'])
    list1_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190712/Success_result_mnet_star_id_190709.xlsx',index=False)
    list2_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190712/title_result_mnet_star_id_190709.xlsx',index=False)    
    list3_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190712/fail_result_mnet_star_id_190709.xlsx',index=False)    

if __name__ == '__main__':
    # CONTENTS = list(zip(df['series_id'].values.tolist(), df['cd_date'].values.tolist(), df['cd_content'].values.tolist(), df['cd_url'].values.tolist(), df['cd_view'].values.tolist()))

    df = pd.read_excel("~/Desktop/mycelebs/WebCrawling/190712/singer_list.xlsx")
    name = df['name']
    pk = df['pk']
    mnet_cd_idx = df['mnet_cd_idx']
    
    with tqdm(total=(EndPoint-StratPoint)) as pbar:
        for idx,row in tqdm(df[StratPoint:EndPoint].iterrows(), ascii=True, desc="rolling in the deep"):
            name = row['name']
            pk = row['pk']
            mnet_cd_idx = row['mnet_cd_idx']
            if mnet_cd_idx == 2:
                # print('없는 아티스트 :' + name)
                Searching(mnet_cd_idx, str(paged))
                continue
            else : 
                paged = Is_it_be(mnet_cd_idx)
                # print('아티스트 : ' + name +':'+ str(paged))
                Searching(mnet_cd_idx, str(paged))
            pbar.update()
    Save_Excel(Success_list, title_list, fail_list)
    cprint('\n Complete Success \n', 'red')        
        


    