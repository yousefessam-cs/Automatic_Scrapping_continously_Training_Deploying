import requests
from bs4 import BeautifulSoup
from datetime import datetime
from unidecode import unidecode


def scrap():
    news = []
    urls = []
    page = 1
    day = datetime.today().strftime('%d')
    while page < 3:
        result = requests.get(f"https://www.presidency.eg/Surface/News/GetAll?startDate=&endDate=&categoryId=-1&pageNumber={page}&culture=ar-EG")

        src = result.content

        soup = BeautifulSoup(src, "lxml")

        articles = soup.find_all("div", {"class": "col-xl-3 col-lg-4 col-md-6 col-sm-6 card-container card-content-columns"})

        for article in articles:
            date = article.find("span", {"class": "date"}).text
            date = unidecode(date).split()[0]
            url = article.find("div", {"class": "card"}).a.attrs['href']
            if day == date:
                urls.append(url)


        page += 1

    for link in urls:
        try:
            result = requests.get(link)

            src = result.content
            soup = BeautifulSoup(src, "lxml")
            header = soup.find("h2", {"class": "header-top-bottom-line"})
            text = soup.find("div", {"class": "details-brief"}).findAll('p')
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
            news.append(news_text)
        except:
            continue

    fake_flag = []

    for i in range(len(news)):
        fake_flag.append(1)

    return news, fake_flag
