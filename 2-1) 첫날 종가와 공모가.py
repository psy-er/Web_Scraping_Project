import inline as inline
import matplotlib
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px

import matplotlib
matplotlib.rcParams['font.family'] ='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] =False

def crawl(url):
    #data = pd.read_html(url, encoding ='euc-kr')
    data = requests.get(url)
    print(data)
    hangul = data.content.decode('euc-kr', 'replace')
    return hangul

def getStockInfo(tr):
    tds = tr.findAll("td")

    aTag = tds[0].find("a")
    name = aTag.text

    first_day = tds[5].text
    first_day = first_day.replace(',','')
    first_day = float(first_day)

    offering_price = tds[2].find("div")
    offering_price_name =offering_price.text
    offering_price_name = offering_price_name.replace(',','')
    offering_price_name = float(offering_price_name)


    return {"name": name, "first_day": first_day , "offering_price_name" : offering_price_name}

def parse(pageString):

    bsObj = BeautifulSoup(pageString, "html.parser")
    box_type_l = bsObj.find("div", {"class": "tbl_head01 tbl_wrap"})
    type_5 = box_type_l.find("table")
    trs = type_5.findAll("tr")

    stockInfos = []

    for tr in trs:
        try:
            stockInfo = getStockInfo(tr)
            stockInfos.append(stockInfo)
            print(stockInfo)
        except Exception as e:
            pass

    return stockInfos

url = "http://iponote.co.kr/ipo/ipo6.php"
pageString = crawl(url)
list = parse(pageString) ##리스트 안에 딕셔너리가 있는 형태이다.
plt.figure(figsize=(10,4))

title = []
for i in range(0,len(list)):
    title.append(list[i]['name'])


df = pd.DataFrame(list,index = title)
df.plot(kind = "bar", stacked =True, figsize = (10,8))
plt.legent(loc = "lower left",bbox_to_anchor = (0.8,1.0))
plt.title(" 첫날 종가와 공모가 ",fontsize = 25)
plt.xlabel('title')
plt.ylabel('gap')
plt.show()