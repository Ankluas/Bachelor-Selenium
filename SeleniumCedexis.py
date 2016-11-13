from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('E:/Programme/chromedriver.exe')
driver.set_page_load_timeout(30)
linkIndex = 0
cedexisCounter = 0
notLoadedCounter = 0

#change directory to your preference
#list of links which are visited by the webdriver searching for the word cedexis in their html code
readList = open("E:/Eigene Dateien/list/list_Test.txt", "r")
#list of all links which contains the word cedexis in their html code
writeList = open("E:/Eigene Dateien/list/cedexisList.txt", "w")

while True:
    try:
        for line in readList:
            if line.strip():
                driver.get(line)
                time.sleep(3)
                html = driver.execute_script("return document.documentElement.outerHTML")
                if (html.find("cedexis") == -1):
                    linkIndex += 1
                    print(linkIndex, "not found")
                else:
                    linkIndex += 1
                    print(linkIndex, "FOUND")
                    writeList.write(str(linkIndex) + " " + line)
                    cedexisCounter += 1
    except:
        TimeoutError
        linkIndex += 1
        notLoadedCounter += 1
        print(linkIndex, "Site couldn't load!")
        continue
    break

readList.close()
writeList.close()
driver.close()
print("Number of sites using Cedexis:", cedexisCounter)
print("Not loaded sites:", notLoadedCounter)
