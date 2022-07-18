import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime
import re

baseURL = "https://www.newyorker.com"


def scrap():
    news = []
    urls = []
    page = 1
    try:
        while page < 2:
            result = requests.get(f"https://www.newyorker.com/humor/borowitz-report/page/{page}")
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            lst = soup.find_all("li", {"class": "River__riverItem___3huWr"})
            for li in lst:
                try:
                    date = li.find("h6", {"class": "River__publishDate___1fSSK"}).text
                    date = str(parse(date, fuzzy=True)).split()[0]
                    today = re.search("\d+:\d+ (P|A)\.M\.")
                    if not today:
                        break
                    url = li.find("div", {"class": "River__riverItemContent___2hXMG"}).a.attrs['href']
                    urls.append(url)
                except:
                    continue
            page += 1
    except:
        return [], []

    for link in urls:
        try:
            result = requests.get(f"{baseURL}{link}")

            src = result.content

            soup = BeautifulSoup(src, "lxml")
            header = soup.find("h1", {"class": "BaseWrap-sc-TURhJ BaseText-fFzBQt ContentHeaderHed-kpvpFG eTiIvU "
                                               "fHXNkq klOfMA"})
            text = soup.find("div", {"class": "body__inner-container"}).findAll('p')
            news_text = f"{header.text.strip()}"
            for p in text:
                news_text += " " + f"{p.text.strip()}"
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
            news.append(news_text.strip())
        except:
            continue

    fake_flag = []

    for i in range(len(news)):
        fake_flag.append(0)

    return news, fake_flag


