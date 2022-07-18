import requests
from bs4 import BeautifulSoup
import re
import csv
from itertools import zip_longest

categories = [
    "/arabic/topics/c719d2el19nt/page/",
    "/arabic/topics/ckdxnj6g4znt/page/",
    "/arabic/topics/c719d2ely7xt/page/",
    "/arabic/topics/cyx5kw7g1j2t/page/",
]
baseURL = "https://www.bbc.com"


def scrap():
    news = []
    urls = []
    for cat in categories:
        page = 1
        while page < 3:
            result = requests.get(baseURL + f"{cat}{page}")
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            li = soup.find_all("article", {"class": "qa-post gs-u-pb-alt+ lx-stream-post gs-u-pt-alt+ gs-u-align-left"})

            for i in range(len(li)):
                date = li[i].find("span", {"class": "qa-post-auto-meta"}).text
                today = re.search("^\d\d?:\d\d?$", date)
                if today:
                    url = li[i].find("a", {"class": "qa-story-cta-link"})
                    try:
                        urls.append(url.attrs["href"])
                    except:
                        continue
                else:
                    break
            page += 1;
    urls = list(dict.fromkeys(urls))
    for i in range(len(urls)):
        result = requests.get(baseURL + urls[i])
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        text = soup.find_all("p", {"class": "bbc-1sy09mr e1cc2ql70"})
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
        if not news.__contains__(news_text):
            news.append(news_text)
    fake_flag = []

    for i in range(len(news)):
        fake_flag.append(1)

    return news, fake_flag

