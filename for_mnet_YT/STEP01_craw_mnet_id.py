#-*- coding: utf-8 -*-
import json
import requests
import pandas as pd
import openpyxl
from pandas import DataFrame
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from tqdm import tqdm
import time
import numpy as np
from urllib.request import urlopen, Request
import pprint

StratPoint = 0 #<----여기에 숫자 넣어주시면 되용!
EndPoint = 2956

s = requests.Session()

df = pd.read_excel("/Users/mycelebs_dev/PycharmProjects/web_clowling/190709/singer_list.xlsx")
result_df = df.loc[:, ['name']] 
pk = df['pk']

rdf_i = 0
try :
    data_list=[]
    fail_data_list=[]
    with tqdm(total=EndPoint - StratPoint) as pbar:
        for idx,row in tqdm(df[StratPoint:EndPoint].iterrows(),desc="rolling in the deep"):
            cd_name=row['name']
            pk = row['pk']

            try:
                
                req2 = s.get(f"http://search.api.mnet.com/search/totalweb?q={cd_name}&sort=r&callback=angular.callbacks._0")
                html2 = req2.text
                html2 = html2[21:]
                html2 = html2[:-1]

                #artistid 따오는것
                dict_html2 = json.loads(html2)
                try : 
                    artist_id = int(dict_html2['data']['artistlist'][0]['artistid'])
                    data={"cd_name":cd_name,"artist_id":artist_id, "pk":pk}
                    data_list.append(data)
                    pbar.update()
                except :
                    data={"cd_name":cd_name,"artist_id":"2", "pk":pk}
                    data_list.append(data)
                    fail_data_list.append(data)
                    pbar.update()
        

            except:
                result_df=pd.DataFrame(data_list,columns=['cd_name','artist_id','pk'])
                result_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190709/333_result_mnet_star_id_190709.xlsx',index=False)
                # driver.close()
                result_df=pd.DataFrame(fail_data_list,columns=['cd_name','artist_id','pk'])
                result_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190709/333_fail_result_mnet_star_id_190709.xlsx',index=False)
except:
    result_df=pd.DataFrame(data_list,columns=['cd_name','artist_id','pk'])
    result_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190709/333_result_mnet_star_id_190709.xlsx',index=False)
    # driver.close()
    result_df=pd.DataFrame(fail_data_list,columns=['cd_name','artist_id','pk'])
    result_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190709/333_fail_result_mnet_star_id_190709.xlsx',index=False)
result_df=pd.DataFrame(data_list,columns=['cd_name','artist_id','pk'])
result_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190709/333_result_mnet_star_id_190709.xlsx',index=False)
# driver.close()
result_df=pd.DataFrame(fail_data_list,columns=['cd_name','artist_id','pk'])
result_df.to_excel(f'/Users/mycelebs_dev/PycharmProjects/web_clowling/190709/333_fail_result_mnet_star_id_190709.xlsx',index=False)