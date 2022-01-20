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
    data = requests.get(url)
    print(data)
    hangul = data.content.decode('euc-kr', 'replace')
    return hangul

def getStockInfo(tr):
    tds = tr.findAll("td")
    rank = tds[0].text
    rank = rank.replace(',','')
    rank = int(rank)

    aTag = tds[1].find("a", {"class": "tltle"})
    name = aTag.text

    f_rate = tds[9].text
    f_rate = f_rate.replace(',','')
    f_rate = float(f_rate)

    return {"rank": rank, "name": name, "f_rate": f_rate}

def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    box_type_l = bsObj.find("div", {"class": "box_type_l"})
    type_5 = box_type_l.find("table", {"class": "type_2"})

    trs = type_5.findAll("tr")

    stockInfos = []

    for tr in trs:
        try:
            stockInfo = getStockInfo(tr)
            stockInfos.append(stockInfo)
            print(stockInfo)
        except Exception as e:
            # print("error")
            pass

    return stockInfos

url = "https://finance.naver.com/sise/sise_quant.nhn"
pageString = crawl(url)
list = parse(pageString)

plt.figure(figsize=(10,4))
df = pd.DataFrame(list)
plt.plot(df['name'],df['f_rate'])
plt.title(" 거래량 상위에서 외국인의 비율 ",fontsize = 25)
plt.xlabel('name')
plt.ylabel('f_rate')
plt.show()