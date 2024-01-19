from bs4 import BeautifulSoup
import csv
import pandas as pd
import requests 
import os


url = input("Enter URL: ")
headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
    
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")


def get_table():
    tables = []
    table_elements = soup.find_all('table')
    for table_element in table_elements:
        table = []
        # Find all rows in the table
        rows = table_element.find_all('tr')

        for row in rows:
            # Find all cells in the row
            cells = row.find_all(['th', 'td'])
            
            # Extract text from each cell and append to the row
            row_data = [cell.get_text(strip=True) for cell in cells]
            
            # Append the row to the table
            table.append(row_data)

        # Append the table to the list of tables
        tables.append(table)

    return tables
def save_to_csv(tables, file_name='output.csv'):
    """
    Save tables to a CSV file.
    
    Parameters:
    - tables (list): A list of tables.
    - file_name (str): The name of the CSV file to save.
    """
    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for table in tables:
            csv_writer.writerows(table)