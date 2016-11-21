from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
# import http
import urllib
# from html.parser import HTMLParser
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
import re


def dealwith(driver):
    html = driver.execute_script("return document.documentElement.outerHTML")
    global linkIndex
    global cedexisCounter
    global failedCounter
    if (html.find("cedexis") == -1):
        # if cedexis wasn't found
        linkIndex += 1
        print(linkIndex, "not found")
    else:
        # if cedexis was found
        linkIndex += 1
        print(linkIndex, "FOUND")
        writeList1.write(str(linkIndex) + " " + line)
        cedexisCounter += 1
        # parse HTML code from variable html in soup
        soup = BeautifulSoup(html, 'html.parser')
        # searching HTML code in script tags and iframe tags for radar and getting the src
        for t in soup.select('script[src*=radar]'):
            if t:
                print(t['src'])
                cedexisLine = t['src']
                cedexisLine = cedexisLine.replace("radar.html", "radar.js")
                driver.get("http:" + cedexisLine)
                versionHTML = driver.execute_script("return document.documentElement.outerHTML")
                soupVersion = BeautifulSoup(versionHTML, 'html.parser')

                # testblock
                # matchObject = re.search(r'(.*) Cedexis (.*?) .*', line)
                # print(matchObject.group())



        for t in soup.select('iframe[src*=radar]'):
            if t:
                print(t['src'])
                cedexisLine = t['src']
                cedexisLine = cedexisLine.replace("radar.js", "radar.html")
                driver.get("http:" + cedexisLine)
                versionHTML = driver.execute_script("return document.documentElement.outerHTML")
                soupVersion = BeautifulSoup(versionHTML, 'html.parser')




driver = webdriver.Chrome('E:/Programme/chromedriver.exe')
driver.set_page_load_timeout(30)
linkIndex = 0
cedexisCounter = 0
failedCounter = 0

# change directory to your preference
# list of links which are visited by the webdriver searching for the word cedexis in their html code
readList = open('E:/Eigene Dateien/list/list_lol.txt', "r")
# list of all links which contains the word cedexis in their html code
writeList1 = open('E:/Eigene Dateien/list/cedexisList.txt', "w")
writeList2 = open('E:/Eigene Dateien/list/versionList.txt', "w")


for line in readList:
    if line.strip():
        try:
            # try to reach website
            req = urllib.request.Request(line)
            urllib.request.urlopen(req)
            # visit website with driver
            driver.get(line)
            time.sleep(3)
            dealwith(driver)
        except urllib.error.URLError:
            # try https
            line = line.replace("http", "https")
            try:
                req = urllib.request.Request(line)
                urllib.request.urlopen(req)
                driver.get(line)
                time.sleep(3)
                dealwith(driver)
            except urllib.error.URLError as e:
                linkIndex += 1
                failedCounter += 1
                print(linkIndex, e.reason)
        except TimeoutError:
            # ignore and search html as usual
            dealwith(driver)
        except Exception:
            # linkIndex += 1
            # failedCounter += 1
            # print(linkIndex, "Failed")
            dealwith(driver)

readList.close()
writeList1.close()
writeList2.close()
driver.quit()
print("Number of sites using Cedexis:", cedexisCounter)
print("Failed Sites:", failedCounter)
