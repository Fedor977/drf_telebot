import requests

API_URL = 'http://localhost:8000/api/'
TOKEN_URL = 'http://localhost:8000/api/token/'
USERNAME = 'admin'
PASSWORD = 'password'


def get_token():
    response = requests.post(TOKEN_URL, data={'username': USERNAME, 'password': PASSWORD})
    return response.json()['access']


TOKEN = get_token()


def get_courses():
    headers = {'Authorization': f'Bearer {TOKEN}'}
    response = requests.get(f'{API_URL}courses/', headers=headers)
    return response.json()
