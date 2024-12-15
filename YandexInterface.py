import requests
import os
from dotenv import load_dotenv

load_dotenv()
yandex_token = os.getenv('yandex_token')


class YAInterface:
    def __init__(self, token, version='v1'):
        self.base_url = f'https://cloud-api.yandex.net/{version}'
        self.headers = {'Authorization': f'OAuth {token}'}

    def create_folder(self, folder_name):
        url = f'{self.base_url}/disk/resources'
        params = {'path': folder_name}
        response = requests.put(url, headers=self.headers, params=params)
        return response

    def delete_folder(self, folder_name):
        url = f'{self.base_url}/disk/resources'
        params = {'path': folder_name, 'permanently': True}
        response = requests.delete(url, headers=self.headers, params=params)
        return response


if __name__ == '__main__':
    ya_disk = YAInterface(yandex_token)
    # ya_disk.create_folder('first_folder')
    print(ya_disk.delete_folder('first_folder'))
