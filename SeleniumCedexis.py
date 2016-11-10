from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('E:/Programme/chromedriver.exe')
driver.set_page_load_timeout(20)
counter = 0
list = open("E:/Eigene Dateien/list/list.txt", "r")

while True:
    try:
        for line in list:
            if line.strip():
                driver.get(line)
                time.sleep(3)
                html = driver.execute_script("return document.documentElement.outerHTML")
                if (html.find("cedexis") == -1):
                    print("not found")
                else:
                    print("FOUND")
                    counter += 1
    except:
        TimeoutError
        print("Site couldn't load!")
        continue
    break


list.close()
driver.close()
print("Number of sites using Cedexis:", counter)
