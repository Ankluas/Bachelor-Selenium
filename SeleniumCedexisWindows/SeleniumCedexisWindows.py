from selenium import webdriver
import time
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import re

# Necessary paramaters:
# - list to read (txt)
# - counter where to start (int)


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
def getCedexisVersion(soup):
    global cedexisCounter
    global cflag
    # searching HTML code in script tags in src attribute for radar and getting the src
    for t in soup.select('script[src*=radar]'):
        if t:
            cflag = 1
            print(t['src'])
            cedexisLine = t['src']
            cedexisLine = cedexisLine.replace("radar.js", "radar.html")
            # calls the radar site
            driver.get("http:" + cedexisLine)
            versionHTML = driver.execute_script("return document.documentElement.outerHTML")
            # searching for version number with regular expressions and write result in cedexisList
            versionString = re.search(r"[0-9]+\.[0-9]+\.[0-9]*", versionHTML)
            if versionString:
                print(versionString)
                cedexisList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + str(cedexisLine) + " " + str(versionString) + " " + line)
                cedexisList.flush()
    # searching HTML code in iframe tags in src attribute for radar and getting the src
    if (cflag == 0):
        for t in soup.select('iframe[src*=radar]'):
            if t:
                print(t['src'])
                cedexisLine = t['src']
                cedexisLine = cedexisLine.replace("radar.js", "radar.html")
                # calls the radar site
                driver.get("http:" + cedexisLine)
                versionHTML = driver.execute_script("return document.documentElement.outerHTML")
                # searching for version number with regular expressions and write result in cedexisList
                versionString = re.search(r"[0-9]+\.[0-9]+\.[0-9]*", versionHTML)
                if versionString:
                    print(versionString)
                    cedexisList.write(str(linkIndex) + " " + "found" + " " + "iframe" + " " + str(cedexisLine) + " " + str(versionString) + " " + line)
                    cedexisList.flush()


# looks for the jquery tag and gets the jQuery version
def getjQueryVersion(soup):
    global jflag
    global jQueryCounter
    # searching HTML code in script tags in src attribute for jQuery and getting the src
    for t in soup.select('script[src*=jquery]'):
        if t:
            jflag = 1
            print(t['src'])
            jQueryLine = t['src']
            # calls the version site
            driver.get(jQueryLine)
            versionHTML = driver.execute_script("return document.documentElement.outerHTML")
            # searching for version number with regular expressions and write result in jQueryList
            versionString = re.search(r"[0-9]+\.[0-9]+\.[0-9]*", versionHTML)
            if versionString:
                print(versionString)
                jQueryList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + str(jQueryLine) + " " + str(versionString) + " " + line)
                jQueryList.flush()
    # searching HTML code in iframe tags in src attribute for radar and getting the src
    if(jflag == 0):
        for t in soup.select('iframe[src*=jQuery]'):
            if t:
                print(t['src'])
                jQueryLine = t['src']
                # calls the version site
                driver.get(jQueryLine)
                versionHTML = driver.execute_script("return document.documentElement.outerHTML")
                # searching for version number with regular expressions and write result in jQueryList
                versionString = re.search(r"[0-9]+\.[0-9]+\.[0-9]*", versionHTML)
                if versionString:
                    print(versionString)
                    jQueryList.write(str(linkIndex) + " " + "found" + " " + "iframe" + " " + str(jQueryLine) + " " + str(versionString) + " " + line)
                    jQueryList.flush()


# checks if the string ember is in a script tag
def checkEmber(soup):
    global emberCounter
    # searching HTML code in script tags in src attribute for ember
    if soup.select('script[src*=ember]'):
        emberCounter += 1
        emberList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + line)
        emberList.flush()


# checks if the string knockout is in a script tag
def checkKnockout(soup):
    global knockoutCounter
    # searching HTML code in script tags in src attribute for knockout
    if soup.select('script[src*=knockout]'):
        knockoutCounter += 1
        knockoutList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + line)
        knockoutList.flush()


# checks if the string backbone is in a script tag
def checkBackbone(soup):
    global backboneCounter
    # searching HTML code in script tags in src attribute for backbone
    if soup.select('script[src*=backbone]'):
        backboneCounter += 1
        backboneList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + line)
        backboneList.flush()


# checks if the string backbone is in a script tag
def checkAngular(soup):
    global angularCounter
    # searching HTML code in script tags in src attribute for angular
    if soup.select('script[src*=angular]'):
        angularCounter += 1
        angularList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + line)
        angularList.flush()


# checks if the string react is in a script tag
def checkReact(soup):
    # searching HTML code in script tags in src attribute for react
    if soup.select('script[src*=react]'):
        reactCounter += 1
        reactList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + line)
        reactList.flush()


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
        if (html.find("knockout") == -1) and (html.find("Knockout") == -1):
            # if Knockout wasn't found
            print(linkIndex, "Knockout not found")
        else:
            # if Knockout was found
            print(linkIndex, "String Knockout FOUND")
            # parse HTML code from variable html in soup
            soup = BeautifulSoup(html, 'html.parser')
            checkKnockout(soup)
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
        if (html.find("backbone") == -1) and (html.find("Backbone") == -1):
            # if Backbone React wasn't found
            print(linkIndex, "Backbone not found")
        else:
            # if Backbone was found
            print(linkIndex, "String Backbone FOUND")
            # parse HTML code from variable html in soup
            soup = BeautifulSoup(html, 'html.parser')
            checkBackbone(soup)
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
        if (html.find("ember") == -1) and (html.find("Ember") == -1):
            # if Ember wasn't found
            print(linkIndex, "Ember not found")
        else:
            # if Ember was found
            print(linkIndex, "String Ember FOUND")
            # parse HTML code from variable html in soup
            soup = BeautifulSoup(html, 'html.parser')
            checkEmber(soup)
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
        if (html.find("react") == -1) and (html.find("React") == -1):
            # if Google React wasn't found
            print(linkIndex, "React not found")
        else:
            # if Google React was found
            print(linkIndex, "String React FOUND")
            # parse HTML code from variable html in soup
            soup = BeautifulSoup(html, 'html.parser')
            checkReact(soup)
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
        if (html.find("angular") == -1) and (html.find("Angular") == -1):
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
        if (html.find("jQuery") == -1) and (html.find("jquery") == -1):
            # if jQuery wasn't found
            print(linkIndex, "jQuery not found")
        else:
            # if jQuery was found
            print(linkIndex, "jQuery FOUND")
            jQueryCounter += 1
            jflag = 0
            # parse HTML code from variable html in soup
            soup = BeautifulSoup(html, 'html.parser')
            getjQueryVersion(soup)
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
        if (html.find("cedexis") == -1) and (html.find("Cedexis") == -1):
            # if cedexis wasn't found
            print(linkIndex, "Cedexis not found")
        else:
            # if cedexis was found
            print(linkIndex, "String Cedexis FOUND")
            cedexisCounter += 1
            cflag = 0
            # parse HTML code from variable html in soup
            soup = BeautifulSoup(html, 'html.parser')
            getCedexisVersion(soup)
    except TimeoutError:
        failedCounter += 1
        print(linkIndex, "TimeoutError")
    except Exception as e:
        failedCounter += 1
        print(linkIndex, str(e))
    except:
        failedCounter += 1
        print(linkIndex, "UNEXPECTED EXCEPTION", sys.exc_info()[0])


# flags which decide if search in iframe is necessary
jflag = 0
cflag = 0
# start index for the websites
linkIndex = int(sys.argv[2])
# counters for the libraries and failed sites
cedexisCounter = 0
angularCounter = 0
jQueryCounter = 0
adSenseCounter = 0
reactCounter = 0
emberCounter = 0
backboneCounter = 0
knockoutCounter = 0
failedCounter = 0
# Windows: change directory to your preference
# list of links which are visited by the webdriver searching for the word cedexis, ... in their html code
readList = open(sys.argv[1], "r")
# lists with all found infos for libraries
cedexisList = open('E:/Eigene Dateien/list/cedexisList.txt', "w")
jQueryList = open('E:/Eigene Dateien/list/jQueryList.txt', "w")
angularList = open('E:/Eigene Dateien/list/angularList.txt', "w")
adSenseList = open('E:/Eigene Dateien/list/adSenseList.txt', "w")
reactList = open('E:/Eigene Dateien/list/reactList.txt', "w")
emberList = open('E:/Eigene Dateien/list/emberList.txt', "w")
backboneList = open('E:/Eigene Dateien/list/backboneList.txt', "w")
knockoutList = open('E:/Eigene Dateien/list/knockoutList.txt', "w")


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
angularList.close()
jQueryList.close()
reactList.close()
emberList.close()
knockoutList.close()
backboneList.close()
driver.quit()
print("Number of sites using Cedexis:", cedexisCounter)
print("Number of sites using jQuery:", jQueryCounter)
print("Number of sites using Angular:", angularCounter)
print("Number of sites using AdSense:", adSenseCounter)
print("Number of sites using React:", reactCounter)
print("Number of sites using Ember:", emberCounter)
print("Number of sites using Backbone:", backboneCounter)
print("Number of sites using Knockout:", knockoutCounter)
print("Failed Sites:", failedCounter)
