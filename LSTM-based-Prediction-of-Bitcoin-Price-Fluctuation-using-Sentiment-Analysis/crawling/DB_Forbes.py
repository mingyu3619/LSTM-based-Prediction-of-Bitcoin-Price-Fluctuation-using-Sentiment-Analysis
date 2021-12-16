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
    string=string.replace(',','')
    s = string.strip()[:3].lower()


    try:
        month = m[s]
        day=string.split()[1]
        year=string.split()[2]
        date_f=str(year)+'-'+str(month)+'-'+str(day)
        return date_f
    except:
        date_f=False
        return date_f
    else:
        return string

##########################################################################################
title=""
paragraph=""
date=""
author=""
press="Forbes"


target_date='2017-01-01'


options=Options()
options.add_argument('disable-infobars')
options.add_argument('enable-automation')
options.add_argument("--no-sandbox")


#https://www.forbes.com/search/?sort=recent&q=bitcoin&sh=650a2e47279f
browser=f"https://www.forbes.com/search/?sort=recent&q=bitcoin"
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
        time.sleep(1)
        driver.find_element_by_css_selector('body > div.main-content.main-content--overflow-visible.main-content--universal-header > main > div.search-content-wrapper > div.search-content.main-content__left-col > div.search-more').click()
        print('see more')
        time.sleep(2)
        #body > div.main - content.main - content - -overflow - visible.main - content - -universal - header > main > div.search - content - wrapper > div.search - content.main - content__left - col > div.search - results > div > article: nth - child(21) > div.stream - item__text > h2 > a
    driver.implicitly_wait(10)
    time.sleep(2)
    try:
        main_links=driver.find_element_by_css_selector('body > div.main-content.main-content--overflow-visible.main-content--universal-header > main > div.search-content-wrapper > div.search-content.main-content__left-col > div.search-results > div > article:nth-child('+str(i)+') > div > h2 > a')
    except Exception as e:
        i=i+1

    driver.implicitly_wait(3)


    main_links.send_keys(Keys.CONTROL + '\n')
    driver.switch_to_window(driver.window_handles[1])                                                                                #####열린창으로 전환
                                                                                                                                     #####열린 창에서 기사 추츨

    my_time = driver.find_elements_by_css_selector('div.body-container > div.article-headline-container > div > div > div > time')  ###시간 찾는 selector
    date = ""
    #print(my_time)
    for t in my_time:
        #print(t.text)
        date = date + t.text

    date = month_string_to_number(date)

    if(date==False):
        driver.close()
        driver.switch_to_window(driver.window_handles[0])                                                                           ##원래창으로 복귀
        driver.implicitly_wait(3)
        i = i + 1
        continue

    date = date[0:10]



    if(target_date>date):                                                                                                               ###목표시간보다 작으면 While문 끝
        break

    my_author = driver.find_elements_by_css_selector('div> div.body-container > div.top-contrib-block > div > div > div > div.fs-author-wrapper > span > a')

    author=""
    for j in my_author:
        author = author + j.text
    #print(author)

    my_titles = driver.find_elements_by_css_selector(
        '#article-stream-0 > div:nth-child(2) > div.body-container > div.article-headline-container > div > h1')  #########제목 저장
    title = ""
    # print(title)
    for t in my_titles:
        #    print(t.text)
        title = title + str(t.text)

    paragraph = ""
    my_paragraph = driver.find_elements_by_css_selector(
        'div.body-container > div.article-body-container > div.article-body.fs-article.fs-responsive-text.current-article > p')
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








