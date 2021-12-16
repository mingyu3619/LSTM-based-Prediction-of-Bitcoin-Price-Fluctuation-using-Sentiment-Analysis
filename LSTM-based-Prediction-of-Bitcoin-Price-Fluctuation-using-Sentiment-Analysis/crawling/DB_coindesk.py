import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time
from textblob import TextBlob
from selenium.webdriver.chrome.options import Options
##########################################################################################


def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    string = string.replace(',', '')
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        month=out
        day=string.split()[1]
        year=string.split()[2]
        date_f=str(year)+'-'+str(month)+'-'+str(day)
        return date_f
    except:
        date_f=False
        return date_f
##########################################################################################
title=""
paragraph=""
date=""
author=""
press="Coindesk"


target_date='2017-01-01'


options=Options()
options.add_argument('disable-infobars')
options.add_argument('enable-automation')
options.add_argument('headless')
options.add_argument('--disable-gpu')



browser=f"https://www.coindesk.com/search?q=bitcoin&s=relevant"
driver = webdriver.Chrome('C:\\Users\\d\\PycharmProjects\\chromedriver.exe',chrome_options=options)
driver.get(browser)
print(browser)
driver.implicitly_wait(10)



i=1
last_height = driver.execute_script("return document.body.scrollHeight")

while(True):
    driver.implicitly_wait(10)
    if(i%10==0):
        while True:  ##무한스크롤
            # Scroll down to bottom                                                      [2]
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
            time.sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            driver.implicitly_wait(3)
            if new_height == last_height:
                break
            last_height = new_height
        driver.implicitly_wait(5)
        driver.find_element_by_css_selector('#__next > div:nth-child(2) > main > section > div > section.page-area-dotted-content > article > div > section > div.list-item-wrapper.button-wrapper').click()
        print('see more')
        time.sleep(5)

    driver.implicitly_wait(10)

    main_links = driver.find_element_by_css_selector('#__next > div:nth-child(2) > main > section > div > section.page-area-dotted-content > article > div > section > div:nth-child('+str(i)+') > div > div.text-content > a:nth-child(2)')
    driver.implicitly_wait(3)


    driver.implicitly_wait(3)
    time.sleep(3)

    main_links.send_keys(Keys.CONTROL + '\n')
    driver.switch_to_window(driver.window_handles[1])                                                                                #####열린창으로 전환
                                                                                                                                     #####열린 창에서 기사 추츨

    # article-566925 > header > div > div > div.white-background-wrapper > div.article-hero-meta-info-wrapper > div > div.article-hero-datetime > time:nth-child(1)
    # article-566925 > header > div > div > div.white-background-wrapper > div.article-hero-meta-info-wrapper > div > div.article-hero-datetime > time:nth-child(3)
    my_time = driver.find_elements_by_css_selector(
        'div.article-hero-datetime > time:nth-child(1)')     #####시간

    date=""
    for t in my_time:
        #print(t.text)
        date = date + t.text
    date = date[0:12]


    date = month_string_to_number(date)


    if(date==False):
        driver.close()
        driver.switch_to_window(driver.window_handles[0])  ##원래창으로 복귀
        driver.implicitly_wait(3)
        i = i + 1
        continue


    date = date[0:10]



    if(target_date>date):
        break

    my_author = driver.find_elements_by_css_selector(                                                                                 ####작가
        'div > section > div.text-block > a > h5')
    author=""
    for j in my_author:
        author = author + j.text
    #print(author)

    # article-567134 > header > div > div > div > div > h1
    titles = driver.find_elements_by_css_selector(                                                                                      ####제목
        'header > div > div > div > div > h1')                                                #########제목 저장
    title = ""
    for t in titles:
        #print(t.text)
        title = title + str(t.text)

    paragraph = ""                                                                                                              ###############본문저장
    my_paragraph = driver.find_elements_by_class_name("article-pharagraph")
    try:
        my_paragraph += driver.find_elements_by_class_name("article-list")
    except Exception as ex:
        pass
    for p in my_paragraph:
        #print(p.text)
        paragraph = paragraph + str(p.text)


    sentiment_value=""
    sentiment_value = TextBlob(paragraph).sentiment.polarity                                                                    #######감성분서값
    #print(sentiment_value)

    news = [press, author, date, sentiment_value, title, [paragraph]]

    f = open(date + ".csv", "a", encoding='utf-8', newline="")
    wdr = csv.writer(f)

    wdr.writerows([news])
    f.close()
    driver.implicitly_wait(10)

    print("date:", date, "i:", i)

    driver.close()
    driver.switch_to_window(driver.window_handles[0])   ##원래창으로 복귀
    driver.implicitly_wait(3)
    i=i+1








