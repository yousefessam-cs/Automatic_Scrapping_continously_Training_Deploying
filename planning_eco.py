import requests
from bs4 import BeautifulSoup
from datetime import datetime

news = []

baseURL = 'https://mcit.gov.eg'

urls = []
# day = datetime.today().strftime('%d')
day = "15"
page = 1
while page < 2:
    result = requests.get(f"https://mped.gov.eg/News/NewsList?typeId=0&lang=ar&pageNum={page}")
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    # url = soup.find_all("div", {"class": "media-button"})
    articles = soup.find_all("div", {"class": "media-item animate-onscroll"})
    for article in articles:
        date = article.find("span", {"class": "newsdate"}).text.split()[0]
        if day != date:
            continue
        try:
            url = article.find("div", {"class": "media-button"}).a.attrs['onclick'].split('\'', 2)[1]
            urls.append(url)
        except:
            continue

    page += 1

length = len(urls)
index = 1
for link in urls:
    # try:
    print(f"{index}/{length}")
    index += 1
    result = requests.get(f"https://mped.gov.eg/singlenews?id={link}&lang=ar")
    print(f"https://mped.gov.eg/singlenews?id={link}&lang=ar")
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    div = soup.find("div", {"class": "col-lg-9 col-md-9 col-sm-8"})

    print(div)
    br =div.find_all("br")
    t=""
    for b in br:
        t+=b.text+' '
    print(t)
    news_text = f"{t.text.strip()}"

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
    if news_text == "":
        continue
    news.append(news_text.strip())
    # except:
    #     continue
print(news)

fake_flag = []

for i in range(len(news)):
    fake_flag.append(1)

