import os.path
import glob
from bs4 import BeautifulSoup
import csv
import lxml

##############################################################################################################
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
    #########################################################################################################################################
date=""
title=""
paragraph=""
news_count=1

my_path="C:\\Users\\d\\PycharmProjects\\coindesk_3_17\\www.coindesk.com"
os.chdir(my_path)
file_lists=os.listdir(my_path)
file_list=glob.glob('*.html')

for item in file_list:
    print('제목: ',item ,"숫자: ", news_count)

    f=open(item,'r',encoding='ISO-8859-1')
    txt=f.read()

    soup=BeautifulSoup(txt,features='xml')
    my_times = soup.select('div.article-hero-datetime > time:nth-child(1)')############시간

    date=""
    for my_time in my_times:
        #print(my_time.text)
        date = date + my_time.text
    date = date[0:12]
    date = month_string_to_number(date)

    print(date)


    titles = soup.select('header > div > div> div > div > h1')                                                           #############제목 저장
    title = ""

    for t in titles:
        #print(t.text)
        title = title + str(t.text)

    i=1
    node='#node-1'

    paragraph = ""                                                                                                                                ###############본문저장
    while(soup.select(node)):

        node = '#node-{}'.format(i)

        my_paragraph = soup.select(node)

        for p in my_paragraph:
            #print(p.text)
            paragraph = paragraph + p.text.replace('\n','')

        i=i+1
    my_paragraph = soup.select('section > section > div.classic-body > p')
    for p in my_paragraph:
        #print(p.text)
        paragraph = paragraph + str(p.text)



    news = [date,title, paragraph]

    f = open("merge_coindesk.csv", "a", encoding='utf-8', newline="")
    wdr = csv.writer(f)
    wdr.writerows([news])
    f.close()
    news_count+=1


#article-409481 > section > section > div.classic-body > p:nth-child(1)
#article-409481 > section > section > div.classic-body > p:nth-child(10)
#article-409481 > section > section > div.classic-body
#article-409481 > section > section > div.classic-body > p:nth-child(1)
#article-409481 > section > section > div.classic-body > p:nth-child(1)
#article-409481 > section > section > div.classic-body > p:nth-child(1)
