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

    aTag = tds[0].find("a")
    name = aTag.text

    gap = tds[4].text
    gap = gap.replace('%','')
    gap = float(gap)


    return {"name": name, "gap": gap }

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
plt.title(" 기업명과 수익 등락률 ",fontsize = 25)
plt.xlabel('title')
plt.ylabel('gap')
plt.show()