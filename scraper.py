import requests
import json
import wget
from bs4 import BeautifulSoup


BASE_URL = 'https://www.filmtypes.com'
FILM_URL = 'https://www.filmtypes.com/films'
FILE_PATH = '/static/images/film/'


def get_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_film_names():
    return get_content(FILM_URL).findAll(class_='film_title')


def get_films():
    films = {}
    for film_name in get_film_names():
        if film_name.text == 'YOUR AD HERE':
            pass
        elif film_name.text == 'More films will be added soon!':
            pass
        else:
            link_name = film_name.text.replace(' ', '-')
            spec_data = get_content(f'{FILM_URL}/{link_name}').findAll(class_='spec_data')
            films[film_name.text] = {
                'link': f'{FILM_URL}/{link_name}',
                'film_type': f'{spec_data[0].text}',
                'brand': f'{spec_data[1].text}',
                'formats': f'{spec_data[2].text}',
                'origin': f'{spec_data[3].text}',
                'process': f'{spec_data[4].text}',
                'film_speed': f'{spec_data[5].text}',
                'grain': f'{spec_data[-5].text}',
                'contrast': f'{spec_data[-4].text}',
                'facts': f'{spec_data[-1].text}',
                'image': f'{FILE_PATH}{link_name.lower()}.jpg'
            }
    return films

def get_film_images():
    image_links = []
    links = get_content(FILM_URL).findAll(class_='filmroll')
    for link in links:
        image_links.append(f'{BASE_URL}{link["src"]}')
    for image_link in image_links:
        file_name = image_link.split('/')[-1].split('.')
        wget.download(image_link, out=f'./static/images/film/{file_name[0]}.{file_name[-1]}')
    return

def get_names():
    names = []
    for film_name in get_film_names():
        if film_name.text == 'YOUR AD HERE':
            pass
        elif film_name.text == 'More films will be added soon!':
            pass
        else:
            names.append(film_name.text)
    return names


def create_json():
    json_object = json.dumps(get_films(), indent=2)
    with open('films.json', 'w') as films_file:
        films_file.write(json_object)

create_json()