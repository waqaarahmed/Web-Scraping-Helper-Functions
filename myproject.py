from bs4 import BeautifulSoup
import csv
import pandas as pd
import requests 
import os
from urllib.parse import urljoin, urlparse
import base64
import imghdr 

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
    file_name = input('Please Enter File Name: ')
    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for table in tables:
            csv_writer.writerows(table)



def get_links():
    links = []
    link_elements = soup.find_all('ahref')
    for link_element in link_elements:
        links.append(link_element)

    filename = input('Please Enter File Name: ')
    with open(filename, 'w', newline='') as f:
         link_writer = csv.writer(f)
         for link in links:
             link_writer.writerow(link)



def get_tags():
    tag_data = []
    tag = input("Enter Tag: ")
    tag_elements = soup.find_all(tag)
    for tag_element in tag_elements:
        tag_data.append(tag_element)
    filename = input('Please Enter File Name: ')
    with open(filename, 'w', newline='') as f:
         tag_writer = csv.writer(f)
         for tag in tag_data:
             tag_writer.writerow(tag)


def get_images(url, save_folder='images'):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Fetch the HTML content of the web page
    response = requests.get(url)
    html_content = response.text

    # Create BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    saved_images = []

    # Find all image elements
    img_elements = soup.find_all('img')

    for img_element in img_elements:
        # Get the source (src) attribute of the image
        img_src = img_element.get('src')

        if img_src:
            # Check if the source is a data URI
            if img_src.startswith('data:image'):
                # Handle data URI (base64-encoded image)
                image_data = img_src.split(',')[1]
                img_data = base64.b64decode(image_data)

                # Generate a filename based on the image type (e.g., 'image/png')
                img_type = imghdr.what(None, h=image_data)
                if not img_type:
                    img_type = 'png'  # Default to PNG if image type cannot be determined

                img_filename = os.path.join(save_folder, f'image_{len(saved_images) + 1}.{img_type}')

                # Save the image to the local filesystem
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_data)

                saved_images.append(img_filename)
            else:
                # Make the URL absolute
                img_url = urljoin(url, img_src)

                # Get the image content
                img_response = requests.get(img_url)

                # Extract the filename from the URL
                img_filename = os.path.join(save_folder, os.path.basename(urlparse(img_url).path))

                # Save the image to the local filesystem
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_response.content)

                saved_images.append(img_filename)

    return saved_images
    return saved_images




get_images(url)