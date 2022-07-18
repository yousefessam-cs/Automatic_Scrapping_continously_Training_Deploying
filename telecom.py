import requests
from bs4 import BeautifulSoup
from datetime import datetime

from unidecode import unidecode

baseURL = 'https://mcit.gov.eg'


def scrap():
    day = datetime.today().strftime('%d')
    urls = []
    news = []
    page = 1

    while page < 2:
        result = requests.get(f"https://mcit.gov.eg/ar/Media_Center/Latest_News/News/filter/0/0/{page}")
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        url = soup.find_all("div", {"class": "media-body"})
        for i in url:
            try:
                urls.append(i.div.a.attrs['href'])
            except:
                continue
        page += 1

    for link in urls:
        try:
            result = requests.get(f"{baseURL}{link}")
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            date = soup.find("span", {"class": "ColoredDate"}).text
            date = unidecode(date).split()[0]
            if day != date:
                break

            news_text = soup.find("div", {"class": "col-md-12 col-sm-12"}).text.strip()
            news_text = news_text.replace('\n', ' ')
            news_text = news_text.replace('\t', ' ')
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
            if news_text == "":
                continue
            news.append(news_text.strip())
        except:
            continue

    fake_flag = []
    for i in range(len(news)):
        fake_flag.append(1)

    return news, fake_flag
