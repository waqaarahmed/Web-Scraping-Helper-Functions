from bs4 import BeautifulSoup
import requests 
import os

url = "https://havenly.com/exp/bedroom-design-ideas"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

links = []
x = soup.select('img[src^="https://images.havenly.com/unsafe"]')
for img in x:
    links.append(img['src'])

for l in links:
    print(l)