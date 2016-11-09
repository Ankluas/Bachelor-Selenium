
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('E:/Programme/chromedriver.exe')

#driver.get("http://dat-berger.de")
driver.get("http://airfrance.fr")
#driver.get("https://www.tumblr.com/")
# driver.get("http://www.lenovo.com/")
time.sleep(3)

html = driver.execute_script("return document.documentElement.outerHTML")
if (html.find("cedexis") == -1):
    print("not found")
else:
    print("found")

driver.close()