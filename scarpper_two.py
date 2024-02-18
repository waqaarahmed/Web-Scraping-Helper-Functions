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
time.sleep(5)

iframe = driver.switch_to.frame("iframe")
accept_button = iframe.find_element(By.XPATH, "//*[@id='uc-center-container']/div[2]/div/div/div/div/button[2]")
time.sleep(3)
accept_button.click()
driver.implicitly_wait(5)