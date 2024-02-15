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
driver.get("https://www.neuralnine.com/")
driver.maximize_window()
time.sleep(10)

links = driver.find_elements(By.XPATH, "//a[@href]")
for link in links:
    if "Books" in link.get_attribute("innerHTML"):
        link.click()
        break
book_links = driver.find_elements(By.XPATH, "//div[contains(@class, 'elementor-coloumn-wrap')][.//h2[text()[contains(., '7 IN 1')]]]")
for book_link in book_links:
    print(book_link.get_attribute("innerHTML"))