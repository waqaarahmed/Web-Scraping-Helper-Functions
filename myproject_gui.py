import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_images(url, save_folder='images'):
    """
    Extract and save all images on a web page.

    Parameters:
    - url (str): The URL of the web page.
    - save_folder (str): The folder where the images will be saved.

    Returns:
    - list: A list of saved image filenames.
    """
    # Create the save folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Fetch the HTML content of the web page
    response = requests.get(url)
    html_content = response.text

    # Create BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all image elements
    img_elements = soup.find_all('img')

    saved_images = []

    for img_element in img_elements:
        # Get the source (src) attribute of the image
        img_src = img_element.get('src')

        if img_src:
            # Make the URL absolute
            img_url = urljoin(url, img_src)

            # Get the image content
            img_response = requests.get(img_url)

            # Extract the filename from the URL
            img_filename = os.path.join(save_folder, os.path.basename(img_url))

            # Save the image to the local filesystem
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_response.content)

            saved_images.append(img_filename)

    return saved_images

url = 'https://havenly.com/exp/bedroom-design-ideas'
saved_images = get_images(url)

print("Images saved:")
for img in saved_images:
    print(img)