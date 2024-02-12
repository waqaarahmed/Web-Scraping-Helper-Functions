from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)
driver.get("https://www.fruitlogistica.com/en/trade-visitors/exhibitor-search/#/search/f=h-entity_orga;v_sg=0;v_fg=0;v_fpa=FUTURE")