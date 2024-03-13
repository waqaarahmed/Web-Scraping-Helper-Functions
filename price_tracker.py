import requests
from bs4 import BeautifulSoup
import time
import datetime
import schedule
import openpyxl

def get_product_price(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the element containing the price
    price_element = soup.find('span', {'class': 'price'})
    
    # Extract the price text
    if price_element:
        price_text = price_element.text.strip()
        return price_text
    else:
        return "Price not found"

def save_to_excel(price, date):
    # Create or load the Excel file
    try:
        wb = openpyxl.load_workbook('price_tracker.xlsx')
    except FileNotFoundError:
        wb = openpyxl.Workbook()

    # Select the active worksheet
    ws = wb.active

    # Append price and date to the next available row
    ws.append([price, date])

    # Save the workbook
    wb.save('price_tracker.xlsx')

def track_price():
    # Get the current date and time
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get the current price
    price = get_product_price("https://example.com/product-page")
    
    # Save price and date to Excel
    save_to_excel(price, current_date)

if __name__ == "__main__":
    # Schedule the script to run daily
    schedule.every().day.at("09:00").do(track_price)  # Adjust the time as per your requirement

    # Run the script continuously
    while True:
        schedule.run_pending()
        time.sleep(1)
