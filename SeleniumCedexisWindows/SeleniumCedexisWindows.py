from selenium import webdriver
import time
import sys
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
# from selenium.webdriver.common.keys import Keys


# try reaching the site with https, if reachable call dealwith()
def tryhttps(driver):
    global linkIndex
    global failedCounter
    global line
    line = line.replace("http", "https")
    try:
        req = urllib.request.Request(line, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            print("HTTPError")
        driver.get(line)
        time.sleep(3)
        dealwith(driver)
    except urllib.error.URLError as e:
        linkIndex += 1
        failedCounter += 1
        print(linkIndex, e.reason)


# looks for the radar tag and gets the cedexis version
def getVersion(soup):
    # searching HTML code in script tags for radar and getting the src
        for t in soup.select('script[src*=radar]'):
            if t:
                print(t['src'])
                cedexisLine = t['src']
                cedexisLine = cedexisLine.replace("radar.js", "radar.html")
                # calls the radar site
                driver.get("http:" + cedexisLine)
                versionHTML = driver.execute_script("return document.documentElement.outerHTML")
                # searching for version number with regular expressions and write result in versionList
                versionString = re.search(r"[0-9]+\.[0-9]+\.[0-9]*", versionHTML)
                if versionString:
                    print(versionString)
                    versionList.write(str(linkIndex) + " " + line + str(versionString) + "\n\n")
        # searching HTML code in iframe tags for radar and getting the src
        for t in soup.select('iframe[src*=radar]'):
            if t:
                print(t['src'])
                cedexisLine = t['src']
                cedexisLine = cedexisLine.replace("radar.js", "radar.html")
                # calls the radar site
                driver.get("http:" + cedexisLine)
                versionHTML = driver.execute_script("return document.documentElement.outerHTML")
                # searching for version number with regular expressions and write result in versionList
                versionString = re.search(r"[0-9]+\.[0-9]+\.[0-9]*", versionHTML)
                if versionString:
                    print(versionString)
                    versionList.write(str(linkIndex) + " " + line + str(versionString) + "\n\n")


# gets the html code of a website and looks for cedexis, if found get the version of cedexis
def dealwith(driver):
    try:
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
            cedexisList.write(str(linkIndex) + " " + line)
            cedexisCounter += 1
            # parse HTML code from variable html in soup
            soup = BeautifulSoup(html, 'html.parser')
            getVersion(soup)

    except TimeoutError:
        linkIndex += 1
        failedCounter += 1
        print(linkIndex, "TimeoutError")

    except Exception as e:
        linkIndex += 1
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        linkIndex += 1
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])


linkIndex = 0
cedexisCounter = 0
failedCounter = 0
# change directory to your preference
# list of links which are visited by the webdriver searching for the word cedexis in their html code
readList = open('E:/Eigene Dateien/list/list_lol.txt', "r")
# list of all links which contains the word cedexis in their html code
cedexisList = open('E:/Eigene Dateien/list/cedexisList.txt', "w")
# list of the index, website and version
versionList = open('E:/Eigene Dateien/list/versionList.txt', "w")


for line in readList:
    driver = webdriver.Chrome('E:/Programme/chromedriver.exe')
    driver.set_page_load_timeout(30)
    if line.strip():
        try:
            # try to reach website
            req = urllib.request.Request(line, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                urllib.request.urlopen(req)
            except urllib.error.HTTPError:
                print("HTTPError")
            # visit website with driver
            driver.get(line)
            time.sleep(3)
            dealwith(driver)
        except urllib.error.URLError:
           # try https function
           tryhttps(driver)
        except TimeoutError:
            linkIndex += 1
            failedCounter += 1
            print(linkIndex, "TimeoutError")
        except Exception as e:
            linkIndex += 1
            failedCounter += 1
            print(linkIndex, str(e))
        except:
            linkIndex += 1
            failedCounter += 1
            print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])
        else:
            print("sucess")
        finally:
            print("end of loop")
            driver.quit()


readList.close()
cedexisList.close()
versionList.close()
print("Number of sites using Cedexis:", cedexisCounter)
print("Failed Sites:", failedCounter)
