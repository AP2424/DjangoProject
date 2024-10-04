import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import requests
from bs4 import BeautifulSoup
from fantasy.models import Club, League

Club.objects.all().delete()

host = "https://www.transfermarkt.com"

heads = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

def get_html(link):
    code = requests.get(link, headers=heads)
    return code.content

def get_teams():
    all_clubs = []
    for obj in League.objects.all():
        content = get_html(obj.url)
        soup = BeautifulSoup(content, 'html.parser')
        clubs = soup.find('div', id='yw1').find_all("tr", class_=['even', 'odd'])
        all_clubs.append(clubs)
    return all_clubs

clubs = get_teams()
for league in clubs:
    for club in league:
        cl = Club(name=club.find_all('a')[1].get_text(),
                  league_id = clubs.index(league) + League.objects.first().id,
                  url = host + club.find_all('a')[1]['href'])
        cl.save()