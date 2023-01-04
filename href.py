# BeautifulSoupをインポート
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import pandas as pd
import time
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#「手っ取り早くPython3.xをダウンロードして使ってみる(Mac)！はじめてのPython」のURLを指定
url = "https://nanpre.adg5.com/xlsx_down.php"

# ページのHTML(ソース)を取得
html = requests.get(url)

# BeautifulSoupで解析(=parser)
soup = BeautifulSoup(html.content, "html.parser")
count=0
countE=0
# aタグを解析データから全て見つけてhref属性の中身を表示
for element in soup.find_all("a"):
    url_tail = element.get("href")
    if re.match(r"xlsx_get.php.*",str(url_tail)):
        url=urljoin("https://nanpre.adg5.com/",url_tail)

        df = pd.read_excel(url,usecols="B:J")

        if len(df) != 18 and len(df.columns) != 9:
            countE+=1
            continue

        df = df.fillna(0)
        df = df.replace(" *",0,regex=True)
        df = df.astype(int)
        df.loc[0:8].to_csv("question.csv", header = False, index = False, mode = 'a')
        df.loc[10:18].to_csv("answer.csv", header = False, index = False, mode = 'a')

        count+=1
        time.sleep(1)
        
    if (count%10)==0:
        print(count)
print("finish")
print(count)
print(countE)
