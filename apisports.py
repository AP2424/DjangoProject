import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import requests

BASE_URL = 'https://v3.football.api-sports.io'
headers = {'x-apisports-host': 'v3.football.api-sports.io/',
           'x-apisports-key': 'b0987c08082614045b1eeeae8010b547'}

for i in range(200):
    response = requests.get(BASE_URL + f'/teams?id={i}', headers=headers)
    print(response.json())