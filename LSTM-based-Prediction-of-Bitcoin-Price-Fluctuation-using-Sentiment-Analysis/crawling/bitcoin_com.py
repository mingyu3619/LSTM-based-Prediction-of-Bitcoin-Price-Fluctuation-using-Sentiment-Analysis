from bs4 import BeautifulSoup,NavigableString,Tag
import requests
import csv

#############################################
##1.title하고 paragraph 같은줄에 안나오는 문제
##2.큰따옴표 꺠짐
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

################################################################
title=""
paragraph=""
date=""
press="BitcoinNews"

for i in range(1,1272):
    browser=f"https://news.bitcoin.com/page/{i}/?s=bitcoin"
    req=requests.get(browser)
    print(browser)
    html=req.text
    soup=BeautifulSoup(html,'html.parser')
    my_titles=soup.select(

        ' div > div > div.item-details>h3>a'                    ########## 하이퍼링크 파싱
    )
    my_time = soup.select(

        ' div > div > div.item-details>div.td-module-meta-info>span>time'             ######날짜 파싱
    )
    j=0
    # td-outer-wrap > div > div > div.td-pb-row > div.td-pb-span8.td-main-content > div > div:nth-child(5) > div.item-details > div.td-module-meta-info > span > time


    for title in my_titles:                                             ######본문있는 링크

        #print(title.get('href'))
        #print(my_time[j].text)
        date=my_time[j].text
        date = month_string_to_number(date)

        f = open(date + ".csv", "a",encoding='utf-8' ,newline="")
        wdr = csv.writer(f)

        j+=1
        browser_in=title.get('href')
        req_in=requests.get(browser_in)
        html = req_in.text
        soup = BeautifulSoup(html, 'html.parser')
        my_titles = soup.select(
            'div > main > article > header > h1')                     ###############제목 파싱
        # ajax-load-more > div.alm-listing.alm-ajax > div > main > article > header > h1
        title=""
        for t in my_titles:
            #print(t.text)
            title=title+str(t.text)
        #print(title)

        paragraph=""
        my_paragraph=soup.select(('article>p'))                         ########두줄 다 본문 파싱 but 순서 좀 틀림(이미지 텍스트 때문에)
        my_paragraph+=soup.select('article>blockquote')



        for p in my_paragraph:

            #print(p.text)
            paragraph=paragraph+str(p.text)

        news=[press,date,title,paragraph]


        wdr.writerows([news])

        f.close()


