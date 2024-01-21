from bs4 import BeautifulSoup
import csv
import pandas as pd
import requests 
import os

def get_url():
    url = input("Enter URL: ")
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")


def get_table(soup):
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
def save_table_to_csv(tables):
    """
    Save tables to a CSV file.
    
    Parameters:
    - tables (list): A list of tables.
    - file_name (str): The name of the CSV file to save.
    """
    file_name = input('Please Enter File Name: ')
    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for table in tables:
            csv_writer.writerows(table)



def get_links(soup):
    links = []
    link_elements = soup.find_all('ahref')
    for link_element in link_elements:
        links.append(link_element)

def save_links_to_csv(links):
     filename = input('Please Enter File Name: ')
     with open(filename, 'w', newline='') as f:
         link_writer = csv.writer(f)
         for link in links:
             link_writer.writerow(link)



def get_tags(soup):
    tag_data = []
    tag = input("Enter Tag: ")
    tag_elements = soup.find_all(tag)
    for tag_element in tag_elements:
        tag_data.append(tag_element)

def save_tags_to_csv(tag_data):
    filename = input('Please Enter File Name: ')
    with open(filename, 'w', newline='') as f:
         tag_writer = csv.writer(f)
         for tag in tag_data:
             tag_writer.writerow(tag)

def get_images(soup):
    