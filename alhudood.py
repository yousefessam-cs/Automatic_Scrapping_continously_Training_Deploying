import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from datetime import datetime

baseURL = "https://alhudood.net"


def scrap():
    news = []
    urls = []
    result = requests.get(baseURL + f"/currentAffairs")
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    articles = soup.find_all("div", {"class": "postBlock_post-content__Jy14G"})
    day = datetime.today().strftime('%d')
    for article in articles:
        try:
            date = article.find("div", {"class": "postBlock_date__qOneZ"}).text
            date = unidecode(date).split()[0]
            url = article.find("h2", {"class": "postBlock_title__FdIbP"}).a.attrs["href"]
            if day == date:
                urls.append(url)
            else:
                break
        except:
            continue

    for url in urls:

        result = requests.get(baseURL + url)
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        news_text = ""
        try:

            text = soup.find("section", {"class": "postBody_post-content__SYatT"}).p
            date = soup.find("p", {"class": "postHeader_post-date__Ag0Kg"})
            for content in text.find_all("span"):
                news_text += content.text
        except:
            continue
        if news_text == "":
            continue
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
        news.append(news_text.strip())

    fake_flag = []
    print(len(news))
    for i in range(len(news)):
        fake_flag.append(0)

    return news, fake_flag
