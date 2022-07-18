import requests
from bs4 import BeautifulSoup
from datetime import datetime


def scrap():
    news = []
    today = datetime.today().strftime('%Y-%m-%d')
    urls = []
    page = 1
    while page < 3:

        result = requests.get(f"https://www.emys.gov.eg/section/7?page={page}")

        src = result.content

        soup = BeautifulSoup(src, "lxml")

        first = soup.find("div", {"class": "home-cat-thumb"}).a.attrs['href']
        url = soup.find_all("div", {"class": "home-cat-content"})

        urls.append(first)
        for i in url:
            try:
                i = i.find("div", {"class": "post-thumb"}).a.attrs['href']
                if i in urls:
                    continue
                urls.append(i)
            except:
                continue
        page += 1

    for link in urls:
        try:

            result = requests.get(link)

            src = result.content

            soup = BeautifulSoup(src, "lxml")
            date = soup.find("ul", {"class": "post-list-info"}).find("li").span.text.split()[0]
            if date != today:
                break
            text = soup.find("div", {"class": "post-detail"}).findAll('p')
            news_text = ""
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
            news_text = news_text.replace(' ', '')
            if news_text == "":
                continue
            news.append(news_text.strip())
        except:
            continue

    fake_flag = []

    for i in range(len(news)):
        fake_flag.append(1)

    return news, fake_flag
