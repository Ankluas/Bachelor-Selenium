from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('E:/Programme/chromedriver.exe')
counter = 0
list = open("E:/Eigene Dateien/list/list.txt", "r")

for line in list:
    if line.strip():
        driver.get(line)
        time.sleep(3)
        html = driver.execute_script("return document.documentElement.outerHTML")
        if (html.find("cedexis") == -1):
            print("not found")
        else:
            print("found")
            counter += 1


list.close()
driver.close()
print(counter)
