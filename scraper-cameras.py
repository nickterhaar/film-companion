import requests
import json
import wget
from bs4 import BeautifulSoup


BASE_URL = 'https://kamerastore.com/collections/camera-database?camera_styles=SubCategory-Film+Cameras&compatibility=Usage-Film&page=5&pf_t_compatibility_and_condition=true'


def get_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_cameras():
    cameras = []
    for camera in get_content(BASE_URL).findAll(class_='card-wrapper'):
        print(camera.find('a').find('span').text[:-9])
        print(camera.find('a')['href'])


get_cameras()