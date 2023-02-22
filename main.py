import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def get_image_url(comics_id):
    url = f'https://xkcd.com/{comics_id}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    print(response.json()['alt'])

    return response.json()['img']


def get_comics_name(image_url):
    splited_url = urlparse(image_url)
    image_name = os.path.basename(splited_url.path)

    return image_name


def save_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()

    image_name = get_comics_name(image_url)

    with open(image_name, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    load_dotenv()

    comics_id = 353
    save_image(get_image_url(comics_id))
