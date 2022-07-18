import requests
from bs4 import BeautifulSoup
from datetime import datetime


def scrap():
    day = datetime.today().strftime('%d')
    news = []
    urls = []
    page = 1
    while page < 2:
        result = requests.get(
            f"https://el-zamalek.com/category/%d9%83%d9%84-%d8%a7%d9%84%d8%a3%d8%ae%d8%a8%d8%a7%d8%b1/page/{page}")
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        url = soup.find_all("a", {"class": "more-link"})
        for i in url:
            try:
                urls.append(i.attrs['href'])
            except:
                continue
        page += 1

    for link in urls:
        try:
            result = requests.get(f"{link}")

            src = result.content

            soup = BeautifulSoup(src, "lxml")
            date = soup.find("span", {"class": "tie-date"}).text.split()[0]
            if day != date:
                break
            header = soup.find("h1", {"class": "name post-title entry-title"}).span
            text = soup.find("div", {"class": "entry"}).findAll('p')
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
        fake_flag.append(1)

    return news, fake_flag
