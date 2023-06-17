import requests
from bs4 import BeautifulSoup

xml_url = 'https://thedarkroom.com/film-sitemap.xml'
xml_page = requests.get(xml_url)
soup = BeautifulSoup(xml_page.content, 'html.parser')
loc_urls = soup.findAll('loc')
urls = []

for loc_url in loc_urls:
    urls.append(loc_url.get_text())

page = requests.get(urls[4])
page_soup = BeautifulSoup(page.content, 'html.parser')
page_title = page_soup.find(class_='page-title')
divs = page_soup.findAll(class_='list')

print(page_title.text)
for div in divs:
    print(div.text)