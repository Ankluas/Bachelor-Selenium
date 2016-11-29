from selenium import webdriver
import time
# from selenium.webdriver.common.keys import Keys
import time
import sys
# import http
import urllib
# from html.parser import HTMLParser
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
import re


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
            writeList1.write(str(linkIndex) + " " + line)
            cedexisCounter += 1
            # parse HTML code from variable html in soup
            soup = BeautifulSoup(html, 'html.parser')
            # searching HTML code in script tags for radar and getting the src
            for t in soup.select('script[src*=radar]'):
                if t:
                    print(t['src'])
                    cedexisLine = t['src']
                    cedexisLine = cedexisLine.replace("radar.html", "radar.js")
                    driver.get("http:" + cedexisLine)
                    #versionHTML = driver.execute_script("return document.documentElement.outerHTML")
                    #soupVersion = BeautifulSoup(versionHTML, 'html.parser')

                    # testblock
                    #versionComment = re.search(r"^[ ]*?\\\\.*?\n")
                    # print(versionComment.group(0))
            # searching HTML code in iframe tags for radar and getting the src
            for t in soup.select('iframe[src*=radar]'):
                if t:
                    print(t['src'])
                    cedexisLine = t['src']
                    cedexisLine = cedexisLine.replace("radar.js", "radar.html")
                    driver.get("http:" + cedexisLine)
                    #versionHTML = driver.execute_script("return document.documentElement.outerHTML")
                    #soupVersion = BeautifulSoup(versionHTML, 'html.parser')
                    #print(soupVersion)
    except TimeoutError:
        linkIndex += 1
        print(linkIndex, "TimeoutError")
        # before: ignore and search html as usual
        # dealwith(driver)
    except Exception as e:
        linkIndex += 1
        print(linkIndex, str(e))
    except:
        linkIndex += 1
        # failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])
        # dealwith(driver)

linkIndex = 0
cedexisCounter = 0
failedCounter = 0

# change directory to your preference
# list of links which are visited by the webdriver searching for the word cedexis in their html code
readList = open("list_Thousand".txt, "r")
# list of all links which contains the word cedexis in their html code
writeList1 = open("cedexisList.txt", "w")
writeList2 = open("versionList.txt", "w")


for line in readList:
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    if line.strip():
        try:
            # try to reach website
            req = urllib.request.Request(line, headers={'User-Agent': 'Mozilla/7.0'})
            try:
                urllib.request.urlopen(req)
            except urllib.error.HTTPError:
                print("HTTPError")
            # visit website with driver
            driver.get(line)
            time.sleep(3)
            dealwith(driver)
        except urllib.error.URLError:
            # try https
            line = line.replace("http", "https")
            try:
                req = urllib.request.Request(line, headers={'User-Agent': 'Mozilla/7.0'})
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
        except TimeoutError:
            linkIndex += 1
            print(linkIndex, "TimeoutError")
            # before: ignore and search html as usual
            # dealwith(driver)
        except Exception as e:
            linkIndex += 1
            print(linkIndex, str(e))
        except:
            linkIndex += 1
            # failedCounter += 1
            print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])
            #dealwith(driver)
        else:
            print("sucess")
        finally:
            print("end of loop")
            driver.quit()

readList.close()
writeList1.close()
writeList2.close()
print("Number of sites using Cedexis:", cedexisCounter)
print("Failed Sites:", failedCounter)
