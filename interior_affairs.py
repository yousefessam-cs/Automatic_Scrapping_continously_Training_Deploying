import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
from itertools import zip_longest

baseURL = "https://moi.gov.eg/"


def scrap():
    urls = []
    news = []
    year = datetime.today().strftime('%Y')
    month = datetime.today().strftime('%m')
    if month[0] == '0': month = month[1]
    day = datetime.today().strftime('%d')
    today = year + "/" + month + "/" + day
    page = 1
    while page < 3:

        result = requests.get(baseURL + f"news?sectionId=1&pageIndex={page}")
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        url = soup.find_all("a", {"class": "btn btn-primary btn-center"})

        for i in range(len(url)):
            temp = url[i].attrs["onclick"]
            temp = temp.split("'", 2)[1]
            urls.append(temp)
        page += 1

    for i in range(len(urls)):
        result = requests.get(baseURL + urls[i])
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        date = soup.find("div", {"class": "dateContainer"}).span.text.strip()
        if not today == date:
            break
        text = soup.find_all("p", {"class": "ql-align-right ql-direction-rtl"})
        if text == []:
            text = soup.find_all("p", {"class": "ql-align-right"})
        news_text = ""
        for index in range(len(text)):
            news_text += text[index].text + " "

        news_text = news_text.replace('\n', ' ')
        news_text = news_text.replace(',', '')
        news_text = news_text.replace('،', '')
        news_text = news_text.replace('\"', '')
        news_text = news_text.replace('\'', '')
        news_text = news_text.replace(':', '')
        news_text = news_text.replace('.', '')
        news_text = news_text.replace(' • ', ' ')
        news_text = news_text.replace('،', '')
        news_text = news_text.replace('\r', '')
        news_text = news_text.replace('\xa0', '')
        news_text = news_text.replace('”', '')
        news_text = news_text.replace('“', '')
        if news_text == "":
            continue
        news.append(news_text)

    fake_flag = []

    for i in range(len(news)):
        fake_flag.append(1)
    return news, fake_flag
