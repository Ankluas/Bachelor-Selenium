from selenium import webdriver
import time
import sys
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import re
# from selenium.webdriver.common.keys import Keys

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
            # searching for version number with regular expressions and write result in versionList
            versionString = re.search(r"[0-9]+\.[0-9]+\.[0-9]*", versionHTML)
            if versionString:
                print(versionString)
                cedexisList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + str(cedexisLine) + " " + str(versionString) + " " + line)
                cedexisList.flush()
        # searching HTML code in iframe tags in src attribute for radar and getting the src
    if (cflag != 1):
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
            #jQueryLine = jQueryLine.replace("radar.js", "radar.html")
            # calls the version site
            driver.get(jQueryLine)
            versionHTML = driver.execute_script("return document.documentElement.outerHTML")
            # searching for version number with regular expressions and write result in versionList
            versionString = re.search(r"[0-9]+\.[0-9]+\.[0-9]*", versionHTML)
            if versionString:
                print(versionString)
                jQueryList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + str(jQueryLine) + " " + str(versionString) + " " + line)
                jQueryList.flush()
    # searching HTML code in iframe tags in src attribute for radar and getting the src
    if(jflag != 1):
        for t in soup.select('iframe[src*=jQuery]'):
            if t:
                print(t['src'])
                jQueryLine = t['src']
                #jQueryLine = jQueryLine.replace("radar.js", "radar.html")
                # calls the version site
                driver.get(jQueryLine)
                versionHTML = driver.execute_script("return document.documentElement.outerHTML")
                # searching for version number with regular expressions and write result in versionList
                versionString = re.search(r"[0-9]+\.[0-9]+\.[0-9]*", versionHTML)
                if versionString:
                    print(versionString)
                    jQueryList.write(str(linkIndex) + " " + "found" + " " + "iframe" + " " + str(jQueryLine) + " " + str(versionString) + " " + line)
                    jQueryList.flush()


# checks if the string ember is in a script tag
def checkEmber(soup):
    global emberCounter
    # searching HTML code in script tags in src attribute for ember
    for t in soup.select('script[src*=ember]'):
        if t:
            emberCounter += 1
            emberLine = t['src']
            emberList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + str(emberLine) + " " + line)
            emberList.flush()


# checks if the string knockout is in a script tag
def checkKnockout(soup):
    global knockoutCounter
    # searching HTML code in script tags in src attribute for knockout
    for t in soup.select('script[src*=knockout]'):
        if t:
            knockoutCounter += 1
            knockoutLine = t['src']
            knockoutList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + str(knockoutLine) + " " + line)
            knockoutList.flush()


# checks if the string backbone is in a script tag
def checkBackbone(soup):
    global backboneCounter
    # searching HTML code in script tags in src attribute for backbone
    for t in soup.select('script[src*=backbone]'):
        if t:
            backboneCounter += 1
            backboneLine = t['src']
            backboneList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + str(backboneLine) + " " + line)
            backboneList.flush()


# checks if the string backbone is in a script tag
def checkAngular(soup):
    global angularCounter
    # searching HTML code in script tags in src attribute for angular
    for t in soup.select('script[src*=backbone]'):
        if t:
            angularCounter += 1
            angularLine = t['src']
            angularList.write(str(linkIndex) + " " + "found" + " " + "script" + " " + str(angularLine) + " " + line)
            angularList.flush()


# checks if the string react is in a script tag
def checkReact(soup):
    # searching HTML code in script tags in src attribute for knockout
        for t in soup.select('script[src*=react]'):
            if t:
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
        if (html.find("knockout") == -1):
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
        if (html.find("backbone") == -1):
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
        if (html.find("ember") == -1):
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
        if (html.find("react") == -1):
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
        if (html.find("jQuery") == -1) and (html.find("jquery") == -1):
            # if jQuery wasn't found
            print(linkIndex, "jQuery not found")
        else:
            # if jQuery was found
            print(linkIndex, "jQuery FOUND")
            jQueryCounter += 1
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
        if (html.find("cedexis") == -1):
            # if cedexis wasn't found
            print(linkIndex, "Cedexis not found")
        else:
            # if cedexis was found
            print(linkIndex, "String Cedexis FOUND")
            cedexisCounter += 1
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


jflag = 0
cflag = 0
linkIndex = int(sys.argv[2])
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
# list of all links which contains the word cedexis in their html code
cedexisList = open('cedexisList.txt', "w")
# same as for cedexis
jQueryList = open('jQueryList.txt', "w")
angularList = open('angularList.txt', "w")
adSenseList = open('adSenseList.txt', "w")
reactList = open('reactList.txt', "w")
emberList = open('emberList.txt', "w")
backboneList = open('backboneList.txt', "w")
knockoutList = open('knockoutList.txt', "w")


for line in readList:
    driver = webdriver.Chrome()
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
