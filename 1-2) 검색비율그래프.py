import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

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

    aTag = tds[1].find("a", {"class": "tltle"})
    name = aTag.text

    search = tds[2].text
    search = search.replace('%','')
    search = float(search)

    return {"name": name, "search": search}

def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    box_type_l = bsObj.find("div", {"class": "box_type_l"})
    type_5 = box_type_l.find("table", {"class": "type_5"})

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

url = "https://finance.naver.com/sise/lastsearch2.nhn"
pageString = crawl(url)
list = parse(pageString)

plt.figure(figsize=(10,4))
df = pd.DataFrame(list)
plt.plot(df['name'],df['search'])
plt.title(" 종목에 따른 검색비율 그래프 ",fontsize = 25)
plt.xlabel('name')
plt.ylabel('search')
plt.show()