import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)
driver.get("https://www.fruitlogistica.com/en/trade-visitors/exhibitor-search/#/search/f=h-entity_orga;v_sg=0;v_fg=0;v_fpa=FUTURE")
driver.maximize_window()
time.sleep(10)

iframes = driver.find_elements(By.TAG_NAME, 'iframe')
for iframe in iframes:
        driver.switch_to.frame(iframe)
        links = driver.find_element(By.XPATH, '//*[@id="uc-center-container"]/div[2]/div/div/div/div/button[2]')
        print("Found it")