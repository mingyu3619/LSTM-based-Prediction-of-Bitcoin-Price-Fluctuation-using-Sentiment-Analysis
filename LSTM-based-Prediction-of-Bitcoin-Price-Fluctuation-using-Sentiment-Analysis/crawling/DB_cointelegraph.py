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
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        month=out
        day=string.split()[1]
        year=string.split()[2]
        date_f=str(year)+'-'+str(month)+'-'+str(day)
        return date_f
    except:
        year=string.split()[0]
        month=string.split()[1]
        day=string.split()[2]
        date_f=str(year)+'-'+str(month)+'-'+str(day)
        return date_f
##########################################################################################
title=""
paragraph=""
date=""
author=""
press="Cointelegraph"


target_date='2017-01-01'


options=Options()
options.add_argument('disable-infobars')
options.add_argument('enable-automation')




browser=f"https://cointelegraph.com/tags/bitcoin"
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
        driver.find_element_by_css_selector('#__layout > div > div.layout__wrp > main > div > div > div.tag-page__rows > div.tag-page__posts-col > div.posts-listing.posts-listing_inline > div> div > button').click()
        print('see more')
        time.sleep(2)

    # __layout > div > div.layout__wrp > main > div > div > div.tag-page__rows > div.tag-page__posts-col > div.posts-listing.posts-listing_inline > ul > li:nth-child(1) > article > div > div.post-card-inline__header > a
    # __layout > div > div.layout__wrp > main > div > div > div.tag-page__rows > div.tag-page__posts-col > div.posts-listing.posts-listing_inline > ul > li:nth-child(2) > article > div > div.post-card-inline__header > a
    # __layout > div > div.layout__wrp > main > div > div > div.tag-page__rows > div.tag-page__posts-col > div.posts-listing.posts-listing_inline > ul > li:nth-child(3) > article > div > div.post-card-inline__header > a
    driver.implicitly_wait(10)
    main_links=driver.find_element_by_css_selector('#__layout > div > div.layout__wrp > main > div > div > div.tag-page__rows > div.tag-page__posts-col > div.posts-listing.posts-listing_inline > ul > li:nth-child('+str(i)+') > article > div > div.post-card-inline__header > a')
    driver.implicitly_wait(3)


    main_links.send_keys(Keys.CONTROL + '\n')
    driver.switch_to_window(driver.window_handles[1])                                                                                #####열린창으로 전환
                                                                                                                                     #####열린 창에서 기사 추츨


    my_times=driver.find_elements_by_css_selector('div.post-meta.post__block.post__block_post-meta > div.post-meta__publish-date > time')###시간 찾는 selector
    # explained-post-page > div > div.explained-post-header > div.explained-post-header__meta > div:nth-child(2)

    date=""
    for my_time in my_times:
        date = my_time.get_attribute(('datetime'))
    print(date)
    if(date==""):
        driver.close()
        driver.switch_to_window(driver.window_handles[0])  ##원래창으로 복귀
        driver.implicitly_wait(3)
        i = i + 1

        continue

    if(target_date>date):                                                                                       ###목표시간보다 작으면 While문 끝
        break

    my_author = driver.find_elements_by_css_selector('div.post-meta.post__block.post__block_post-meta > div.post-meta__author > a > div.post-meta__author-name')                                                                                 ####작가

    author=""
    for j in my_author:
        author = author + j.text
    print(author)


    titles = driver.find_elements_by_css_selector('h1')                                                                                      ####제목

    title = ""
    for t in titles:
        #print(t.text)
        title = title + str(t.text)

    paragraph = ""
    my_paragraph = driver.find_elements_by_css_selector('div.post__block.post__block_lead-text')
    my_paragraph = my_paragraph + driver.find_elements_by_css_selector('div.post__content-wrapper > div.post-content')
    # print(paragraph)
    for p in my_paragraph:
        #    print(p.text)
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


    print("date:",date ,"i:",i)

    driver.close()
    driver.switch_to_window(driver.window_handles[0])   ##원래창으로 복귀
    driver.implicitly_wait(3)
    i=i+1








