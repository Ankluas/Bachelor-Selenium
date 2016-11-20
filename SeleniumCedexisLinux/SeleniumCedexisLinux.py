from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
# import http
import urllib


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
        writeList.write(str(linkIndex) + " " + line)
        cedexisCounter += 1


driver = webdriver.Chrome()
driver.set_page_load_timeout(30)
linkIndex = 0
cedexisCounter = 0
failedCounter = 0

# change directory to your preference
# list of links which are visited by the webdriver searching for the word cedexis in their html code
readList = open("list_Test.txt", "r")
# list of all links which contains the word cedexis in their html code
writeList = open("cedexisList.txt", "w")


for line in readList:
    if line.strip():
        try:
            # try to reach website
            req = urllib.request.Request(line)
            urllib.request.urlopen(req)
            # visit website
            driver.get(line)
            time.sleep(3)
            dealwith(driver)
        except urllib.error.URLError:
            # try https
            newLine = line.replace("http", "https")
            try:
                req = urllib.request.Request(newLine)
                urllib.request.urlopen(req)
                driver.get(newLine)
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
            #linkIndex += 1
            #failedCounter += 1
            #print(linkIndex, "Failed")
            dealwith(driver)

readList.close()
writeList.close()
driver.quit()
print("Number of sites using Cedexis:", cedexisCounter)
print("Failed Sites:", failedCounter)
