from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import requests

# study.ai_172@mail.ru
# NextPassword172#
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(10)

driver.get('https://mail.ru')

elem = driver.find_element(By.CLASS_NAME, 'email-input')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)

# elem = driver.find_element(By.CLASS_NAME, 'button')
# elem.click()

elem = driver.find_element(By.CLASS_NAME, 'password-input')
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)
print()



# elem = driver.find_element(By.CLASS_NAME, 'second-button')
# elem.click()
#
# elem = driver.find_element(By.XPATH, "//nav[contains(@class,'nav nav_short')]/a[2]")
# elem.click()

news = driver.find_element(By.XPATH, "//div[@class='dataset__items']/a[contains(@class, 'llc')]/text")
print()