import requests
import json
from bs4 import BeautifulSoup


BASE_URL = 'https://www.filmtypes.com/films'


def get_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_film_names():
    return get_content(BASE_URL).findAll(class_='film_title')


def get_films():
    films = {}
    for film_name in get_film_names():
        if film_name.text == 'YOUR AD HERE':
            pass
        elif film_name.text == 'More films will be added soon!':
            pass
        else:
            link_name = film_name.text.replace(' ', '-')
            spec_data = get_content(f'{BASE_URL}/{link_name}').findAll(class_='spec_data')
            films[film_name.text] = {
                'link': f'{BASE_URL}/{link_name}',
                'film_type': f'{spec_data[0].text}',
                'brand': f'{spec_data[1].text}',
                'formats': f'{spec_data[2].text}',
                'origin': f'{spec_data[3].text}',
                'process': f'{spec_data[4].text}',
                'film_speed': f'{spec_data[5].text}',
                'grain': f'{spec_data[-5].text}',
                'contrast': f'{spec_data[-4].text}',
                'facts': f'{spec_data[-1].text}'
            }
    return films


def get_names():
    names = []
    for film_name in get_film_names():
        if film_name.text == 'YOUR AD HERE':
            pass
        elif film_name.text == 'More films will be added soon!':
            pass
        else:
            names.append(film_name.text)


def create_json():
    json_object = json.dumps(get_films(), indent=2)
    with open('films.json', 'w') as films_file:
        films_file.write(json_object)

create_json()