from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
from itertools import zip_longest

urls = []
news = []
page = 2
while page < 101:
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.minimize_window()
    driver.get(f"https://www.alahlyegypt.com/ar/news/football?page={page}")

    news_list = driver.find_elements(by=By.XPATH, value='//*[@id="postsContainer"]/div/a')

    for div in news_list:
        urls.append(div.get_attribute('href'))
    driver.quit()
    page += 1

for url in urls:
    try:
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.minimize_window()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        news_text = driver.find_element(by=By.XPATH, value='/html/body/section[1]/div[3]/p').text
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
        driver.quit()
    except:
        driver.quit()
        continue

print(news)

fake_flag = []

for i in range(len(news)):
    fake_flag.append(1)

file_list = [news, fake_flag]
exported = zip_longest(*file_list)
with open("alahly.csv","a", newline='', encoding="utf-8") as myfile:
    wr = csv.writer(myfile)
    # wr.writerow(["claim_s", "fake_flag"])
    wr.writerows(exported)
