import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Set up the Selenium WebDriver
url = "https://www.fruitlogistica.com/en/trade-visitors/exhibitor-search/#/search/f=h-entity_orga;v_sg=0;v_fg=0;v_fpa=FUTURE      https://www.biv.be/vastgoedmakelaars?location=1000"
driver = webdriver.Chrome()  # You need to have ChromeDriver installed and in your PATH
driver.get(url)

# Wait for the page to load (you might need to adjust the time based on your internet speed)
driver.implicitly_wait(10)

# Scroll to the bottom of the page to load all exhibitors
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Wait for the page to load after scrolling
driver.implicitly_wait(10)

# Get the page source after scrolling to get all the exhibitors
page_source = driver.page_source

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(page_source, 'html.parser')

# Find and extract information
company_data = []
company_elements = soup.find_all('div', class_='exhibitor__title')
for company_element in company_elements:
    company_name = company_element.text.strip()
    company_data.append({"Company Name": company_name})

# Close the WebDriver
driver.quit()

# Save to CSV
csv_file_path = "fruitlogistica_companies.csv"
fieldnames = ["Company Name"]

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the data
    writer.writerows(company_data)

print(f"Data has been saved to {csv_file_path}")
