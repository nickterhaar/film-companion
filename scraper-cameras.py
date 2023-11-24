import requests
import json
import wget
from bs4 import BeautifulSoup


def get_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_canon_camera_links():
    url = 'https://global.canon/en/c-museum/camera.html?s=film'
    canon_camera_links = []
    for camera in get_content(url).findAll(class_='product_box'):
        if 'film' in camera.find('a')['href']:
            canon_camera_links.append(f"https://global.canon{camera.find('a')['href']}")
    return canon_camera_links


def get_canon_camera_info():
    canon_camera_list = []
    for url in get_canon_camera_links():
        camera_page = get_content(url)
        camera = {}
        
        camera_names = []
        for name in camera_page.findAll(class_='title_i'):
            camera_names.append(name.text)
        camera['names'] = camera_names
        
        print(camera_page.find('tab2'))
        # for row in table.tbody.find_all('tr'):
        #     columns = row.find_all('td')

        #     if columns != []:
        #         print(columns[0].text)


get_canon_camera_info()