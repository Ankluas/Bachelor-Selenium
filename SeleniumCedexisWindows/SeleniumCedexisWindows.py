from selenium import webdriver
import time
import sys
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
# from selenium.webdriver.common.keys import Keys


# try reaching the site with https, if reachable call dealwithAll(driver)
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
        dealwithAll(driver)
    except urllib.error.URLError as e:
        linkIndex += 1
        failedCounter += 1
        print(linkIndex, e.reason)


# looks for the radar tag and gets the cedexis version
def getVersion(soup):
    # searching HTML code in script tags for radar and getting the src
        for t in soup.select('script[src*=radar]'):
            if t:
                srcList.write(str(linkIndex) + " " + "script \n")
                srcList.flush()
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
                    versionList.flush()
        # searching HTML code in iframe tags for radar and getting the src
        for t in soup.select('iframe[src*=radar]'):
            if t:
                srcList.write(str(linkIndex) + " " + "iframe \n")
                srcList.flush()
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
                versionList.flush()


def dealwithAll(driver):
    global linkIndex
    try:
        linkIndex += 1
        dealwithCedexis(driver)
        dealwithjQuery(driver)
        dealwithAngular(driver)
        dealwithAdSense(driver)
        dealwithReact(driver)
        dealwithEmber(driver)
        dealwithBackbone(driver)
        dealwithKnockout(driver)
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])


def dealwithKnockout(driver):
    try:
        html = driver.execute_script("return document.documentElement.outerHTML")
        global linkIndex
        global knockoutCounter
        global failedCounter
        if (html.find("knockout") == -1):
            # if Knockout wasn't found
            print(linkIndex, "Knockout not found")
        else:
            # if Knockout was found
            print(linkIndex, "Knockout FOUND")
            knockoutList.write(str(linkIndex) + " " + line)
            knockoutList.flush()
            knockoutCounter += 1
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])

def dealwithBackbone(driver):
    try:
        html = driver.execute_script("return document.documentElement.outerHTML")
        global linkIndex
        global backboneCounter
        global failedCounter
        if (html.find("backbone") == -1):
            # if Backbone React wasn't found
            print(linkIndex, "Backbone not found")
        else:
            # if Backbone React was found
            print(linkIndex, "Backbone FOUND")
            backboneList.write(str(linkIndex) + " " + line)
            backboneList.flush()
            backboneCounter += 1
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])

def dealwithEmber(driver):
    try:
        html = driver.execute_script("return document.documentElement.outerHTML")
        global linkIndex
        global emberCounter
        global failedCounter
        if (html.find("ember") == -1):
            # if Ember React wasn't found
            print(linkIndex, "Ember not found")
        else:
            # if Ember React was found
            print(linkIndex, "Ember FOUND")
            emberList.write(str(linkIndex) + " " + line)
            emberList.flush()
            emberCounter += 1
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])


def dealwithReact(driver):
    try:
        html = driver.execute_script("return document.documentElement.outerHTML")
        global linkIndex
        global reactCounter
        global failedCounter
        if (html.find("react") == -1):
            # if Google React wasn't found
            print(linkIndex, "React not found")
        else:
            # if Google React was found
            print(linkIndex, "React FOUND")
            reactList.write(str(linkIndex) + " " + line)
            reactList.flush()
            reactCounter += 1
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])

def dealwithAdSense(driver):
    try:
        html = driver.execute_script("return document.documentElement.outerHTML")
        global linkIndex
        global adSenseCounter
        global failedCounter
        if (html.find("adsbygoogle") == -1):
            # if Google Adsense wasn't found
            print(linkIndex, "Adsense not found")
        else:
            # if Google Adsense was found
            print(linkIndex, "Adsense FOUND")
            adSenseList.write(str(linkIndex) + " " + line)
            adSenseList.flush()
            adSenseCounter += 1
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])

def dealwithAngular(driver):
    try:
        html = driver.execute_script("return document.documentElement.outerHTML")
        global linkIndex
        global angularCounter
        global failedCounter
        if (html.find("angular") == -1):
            # if Angular wasn't found
            print(linkIndex, "Angular not found")
        else:
            # if Angular was found
            print(linkIndex, "Angular FOUND")
            angularList.write(str(linkIndex) + " " + line)
            angularList.flush()
            angularCounter += 1
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])


def dealwithjQuery(driver):
    try:
        html = driver.execute_script("return document.documentElement.outerHTML")
        global linkIndex
        global jQueryCounter
        global failedCounter
        if ((html.find("jquery") == -1) or (html.find("jQuery") == -1)):
            # if jQuery wasn't found
            print(linkIndex, "jQuery not found")
        else:
            # if jQuery was found
            print(linkIndex, "jQuery FOUND")
            jQueryList.write(str(linkIndex) + " " + line)
            jQueryList.flush()
            jQueryCounter += 1
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])


# gets the html code of a website and looks for cedexis, if found get the version of cedexis
def dealwithCedexis(driver):
    try:
        html = driver.execute_script("return document.documentElement.outerHTML")
        global linkIndex
        global cedexisCounter
        global failedCounter
        if (html.find("cedexis") == -1):
            # if cedexis wasn't found
            print(linkIndex, "Cedexis not found")
        else:
            # if cedexis was found
            print(linkIndex, "Cedexis FOUND")
            cedexisList.write(str(linkIndex) + " " + line)
            cedexisList.flush()
            cedexisCounter += 1
            # parse HTML code from variable html in soup
            soup = BeautifulSoup(html, 'html.parser')
            getVersion(soup)
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])


linkIndex = 0
cedexisCounter = 0
angularCounter = 0
jQueryCounter = 0
adSenseCounter = 0
reactCounter = 0
emberCounter = 0
backboneCounter = 0
knockoutCounter = 0
failedCounter = 0
# change directory to your preference
# list of links which are visited by the webdriver searching for the word cedexis, ... in their html code
readList = open('E:/Eigene Dateien/list/list_Test.txt', "r")
# list of all links which contains the word cedexis in their html code
cedexisList = open('E:/Eigene Dateien/list/cedexisList.txt', "w")
# list of the index, website and version
versionList = open('E:/Eigene Dateien/list/versionList.txt', "w")
# same as for cedexis
jQueryList = open('E:/Eigene Dateien/list/jQueryList.txt', "w")
angularList = open('E:/Eigene Dateien/list/angularList.txt', "w")
adSenseList = open('E:/Eigene Dateien/list/adSenseList.txt', "w")
reactList = open('E:/Eigene Dateien/list/reactList.txt', "w")
emberList = open('E:/Eigene Dateien/list/emberList.txt', "w")
backboneList = open('E:/Eigene Dateien/list/backboneList.txt', "w")
knockoutList = open('E:/Eigene Dateien/list/knockoutList.txt', "w")
# found in iframe or script
srcList = open('E:/Eigene Dateien/list/srcList.txt', "w")

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
            dealwithAll(driver)
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
angularList.close()
jQueryList.close()
reactList.close()
emberList.close()
knockoutList.close()
backboneList.close()
srcList.close()
print("Number of sites using Cedexis:", cedexisCounter)
print("Number of sites using jQuery:", jQueryCounter)
print("Number of sites using Angular:", angularCounter)
print("Number of sites using AdSense:", adSenseCounter)
print("Number of sites using React:", reactCounter)
print("Number of sites using Ember:", emberCounter)
print("Number of sites using Backbone:", backboneCounter)
print("Number of sites using Knockout:", knockoutCounter)
print("Failed Sites:", failedCounter)
