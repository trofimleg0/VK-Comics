import os
import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse


def get_args():
    parser = argparse.ArgumentParser(description='Pick the comic url')
    parser.add_argument('comic_url', nargs='?', default=get_random_comic_url())

    return parser.parse_args().comic_url


def get_random_comic_url():
    url_random_comic = 'https://c.xkcd.com/random/comic/'

    response = requests.get(url_random_comic)
    response.raise_for_status()

    return response.url


def get_comic_params(comic_url):
    url = f'{comic_url}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    return response.json()['img'], response.json()['alt']


def get_comic_name(image_url):
    splited_url = urlparse(image_url)
    image_name = os.path.basename(splited_url.path)

    return image_name


def save_image(file_path, image_url):
    response = requests.get(image_url)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_image_upload_address(vk_url, access_token, api_version):
    url = f'{vk_url}photos.getWallUploadServer'
    params = {
        'access_token': access_token,
        'v': api_version,
        'group_id': group_id
    }

    response = requests.post(url, params=params)
    response.raise_for_status()

    return response.json()['response']['upload_url']


def upload_image_to_server(image_upload_address, file_path):
    with open(file_path, 'rb') as photo:
        files = {'photo': photo}

        response = requests.post(image_upload_address, files=files)
        response.raise_for_status()

        return response.json()['server'], response.json(
        )['photo'], response.json()['hash']


def save_image_to_vk(vk_url, access_token, api_version, group_id, server_id,
                     photos, image_hash):
    url = f'{vk_url}photos.saveWallPhoto'
    params = {
        'access_token': access_token,
        'v': api_version,
        'group_id': group_id,
        'server': server_id,
        'photo': photos,
        'hash': image_hash
    }

    response = requests.post(url, params=params)
    response.raise_for_status()

    return response.json()['response'][0]['owner_id'], response.json(
    )['response'][0]['id']


def post_comic_in_group(vk_url, access_token, api_version, group_id,
                        image_comment, owner_id, media_id):
    url = f'{vk_url}wall.post'
    post_from_group = 1
    attachments = [f'photo{owner_id}_{media_id}']
    group_id = f'-{group_id}'

    params = {
        'access_token': access_token,
        'v': api_version,
        'owner_id': group_id,
        'from_group': post_from_group,
        'message': image_comment,
        'attachments': attachments
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    load_dotenv()

    group_id = os.environ['GROUP_ID']
    access_token = os.environ['ACCESS_TOKEN']

    image_path = os.environ['IMAGE_PATH']
    Path(image_path).mkdir(parents=True, exist_ok=True)

    comic_url = get_args()
    image_url, image_comment = get_comic_params(comic_url)
    image_name = get_comic_name(image_url)

    file_path = f'{image_path}{image_name}'
    save_image(file_path, image_url)

    vk_url = 'https://api.vk.com/method/'
    api_version = '5.131'

    image_upload_address = get_image_upload_address(vk_url, access_token,
                                                    api_version)

    server_id, photos, image_hash = upload_image_to_server(
        image_upload_address, file_path)

    owner_id, media_id = save_image_to_vk(vk_url, access_token, api_version,
                                          group_id, server_id, photos,
                                          image_hash)

    post_comic_in_group(vk_url, access_token, api_version, group_id,
                        image_comment, owner_id, media_id)
