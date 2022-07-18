import requests
from bs4 import BeautifulSoup
import re
import json


def scrap():
    news = []
    urls = []
    cat = ['8467c0e0-584b-41de-9682-756b311216b5', 'cb393f1f-b04a-4f63-b922-45e4b538f791',
           'e82ae4e3-7a51-4c2c-bf29-44bbebee7f52', 'e72f8215-86a8-4064-932b-918d6c3d73f6',
           '499e1752-327e-4758-9d94-98d3c14d95fb']
    for c in cat:
        for page in range(1, 3):

            request = requests.get(
                f"https://push.api.bbci.co.uk/batch?t=%2Fdata%2Fbbc-morph-lx-commentary-data-paged%2Fabout%2F{c}%2FisUk%2Ffalse%2Flimit%2F20%2FnitroKey%2Flx-nitro%2FpageNumber%2F{page}%2Fversion%2F1.5.6?timeout=5")

            jsonX = json.loads(request.text)

            for x in jsonX['payload'][0]['body']['results']:
                try:
                    if 'media' not in x.keys():
                        if x['url'] not in urls:
                            urls.append(x['url'])
                except:
                    continue

    for link in urls:
        try:

            result = requests.get(f"https://www.bbc.com{link}")

            src = result.content
            soup = BeautifulSoup(src, "lxml")
            date = ""
            if soup.find("time", {"data-testid": "timestamp"}):
                date = soup.find("time", {"data-testid": "timestamp"}).text
            if soup.find("span", {"class": "qa-status-date-output"}):
                date = soup.find("span", {"class": "qa-status-date-output"}).text

            date = str(date)
            today = re.match("(^\d+\s(hours?|minutes?)\sago)|Just\snow", date)

            if not today:
                continue
            header, text = "", []
            if soup.find("article", {"class": "ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6"}):
                soup = soup.find("article", {"class": "ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6"})
                header = soup.find("h1", {"class": "ssrcss-15xko80-StyledHeading e1fj1fc10"})
                text = soup.findAll("p", {"class": "ssrcss-1q0x1qg-Paragraph eq5iqo00"})

            if soup.find("div",
                         {"class": "qa-story-body story-body gel-pica gel-10/12@m gel-7/8@l gs-u-ml0@l gs-u-pb++"}):
                text = soup.find("div", {
                    "class": "qa-story-body story-body gel-pica gel-10/12@m gel-7/8@l gs-u-ml0@l gs-u-pb++"}).find_all(
                    'p')

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
            print(f"https://www.bbc.com{link}")
            continue


    fake_flag = []

    for i in range(len(news)):
        fake_flag.append(1)

    return news, fake_flag

