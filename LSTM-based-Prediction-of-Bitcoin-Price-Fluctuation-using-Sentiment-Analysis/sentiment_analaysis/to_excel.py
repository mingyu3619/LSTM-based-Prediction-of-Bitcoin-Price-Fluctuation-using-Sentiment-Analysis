import csv
import os.path
import glob
import datetime
from textblob import TextBlob
from time import strptime
import time
###########################################################################################################################
date=""

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
#################################################################### 날짜

os.chdir('C:\\Users\\d\\PycharmProjects\\bitcoin_com')
file_lists=os.listdir()
file_list=glob.glob('*.csv')

print(os.getcwd())

for item in file_list:

    print("item: ",item)
    date_before=item.replace('.csv','').replace(',','').replace('-',' ')
    print(date_before)


    date=month_string_to_number(date_before)
    print(date)



    f=open(item,'r',encoding='utf-8',newline="")
    f_sent = open("sentiment_analysis.csv", "a", encoding='utf-8', newline="")  ###########파일저장
    wdr_sent=csv.writer(f_sent)
    lines=f.readlines()
    for line in lines:
        good_news=0
        bad_news=0
        #print(line)
        sentiment_value=TextBlob(line).sentiment.polarity
        if(sentiment_value==0):
            continue
        if(sentiment_value<0):
            bad_news=1
        if(sentiment_value>0):
            good_news=1
        print(sentiment_value)
        news=[date,sentiment_value,good_news,bad_news]
        wdr_sent.writerows([news])




    #wdr.writerows([news])
    f.close()
