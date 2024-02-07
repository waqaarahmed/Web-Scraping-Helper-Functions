import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC



url = "https://www.fruitlogistica.com/en/trade-visitors/exhibitor-search/#/search/f=h-entity_orga;v_sg=0;v_fg=0;v_fpa=FUTURE"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(40)

accept_button = driver.find_element(By.CSS_SELECTOR, "button.sc-dcJsrY:nth-child(2)")
time.sleep(3)
accept_button.click()
driver.implicitly_wait(5)