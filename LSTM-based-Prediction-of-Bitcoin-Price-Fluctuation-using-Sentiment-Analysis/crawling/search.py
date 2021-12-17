import numpy as np
from selenium import webdriver
import csv
import calendar
import time
import random
##################################################################
arr = []

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


driver = webdriver.Chrome('C:\\Users\\d\\PycharmProjects\\chromedriver.exe')
#driver = webdriver.Chrome('C:\\Users\\d\\PycharmProjects\\chromedriver.exe')

PROXY = "115.91.83.42:4145" # IP:Port
webdriver.DesiredCapabilities.CHROME['proxy'] = {                   ##프록시 바꾸기
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL"
}

driver.implicitly_wait(3)

for i in range(2020,2021):
    for j in range(3,4):


        time.sleep(random.randrange(3))
        header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\AppleWebKit 537.36 (KHTML, like Gecko) Chrome","Accept": "text/html,application/xhtml+xml,application/xml;\q=0.9,imgwebp,*/*;q=0.8"}
        browser=f"https://www.google.com/search?q=bitcoin+after:{str(i)}-{str(j).zfill(2)}-01+before:{str(i)}-{str(j+1).zfill(2)}-01&safe=active&tbm=nws&ei=ZDUQX62cBdGXr7wPrMi0MA&start=0&sa=N&ved=0ahUKEwit3rmV0dHqAhXRy4sBHSwkDQY4ChDy0wMIaQ&biw=929&bih=888&dpr="
        driver.get('https://www.google.com/search?q=bitcoin+after:'+str(i)+'-'+str(j).zfill(2)+'-01+before:'+str(i)+'-'+str(j+1).zfill(2)+'-01&safe=active&tbm=nws&ei=ZDUQX62cBdGXr7wPrMi0MA&start=0&sa=N&ved=0ahUKEwit3rmV0dHqAhXRy4sBHSwkDQY4ChDy0wMIaQ&biw=929&bih=888&dpr=1')
        #url=header+browser

        print(browser)
        driver.get(browser)
        driver.implicitly_wait(10)

        del arr[:]
        count = 0

        while('//*[@id="pnnext"]/span[2]'):

            title = driver.find_elements_by_css_selector('div > g-card > div > div > div.dbsr > a > div > div.hI5pFf > div.XTjFC.WF4CUc')
            #title+=driver.find_elements_by_css_selector('div > g-card > div > div > div.dbsr > a > div > div.XTjFC.WF4CUc')
            driver.implicitly_wait(10)
            #nexturl = driver.find_elements_by_css_selector('#pnnext > span:nth-child(2)')




            for l in title:
                count += 1
                print(count , l.text)



                arr.append(l.text)



            try:
                time.sleep(random.randrange(10,13))
                driver.implicitly_wait(5)
                driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]').click()
                driver.implicitly_wait(5)
                ##다음버튼 클릭
            except Exception as ex:
                break


        f = open("test."+str(i)+'-'+str(j).zfill(2)+".csv", "w", encoding='utf-8', newline='')
        wdr = csv.writer(f)

        for l in range(arr.__len__()):
            wdr.writerow([arr[l]])

        f.close()





#//*[@id="pnnext"]/span[2]
#rso > div:nth-child(6) > g-card > div > div > div.dbsr > a > div > div.hI5pFf > div.XTjFC.WF4CUc
#rso > div:nth-child(7) > g-card > div > div > div.dbsr > a > div > div.hI5pFf > div.XTjFC.WF4CUc
#rso > div:nth-child(9) > g-card > div > div > div.dbsr > a > div > div.hI5pFf > div.XTjFC.WF4CUc
#rso > div:nth-child(10) > g-card > div > div > div.dbsr > a > div > div.XTjFC.WF4CUc