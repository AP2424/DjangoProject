import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import requests
from bs4 import BeautifulSoup
from fantasy.models import Player, Club


host = "https://www.transfermarkt.com"
url = "https://www.transfermarkt.com/transfers/neuestetransfers/statistik?land_id=0&wettbewerb_id=alle&minMarktwert=500000&maxMarktwert=200000000&plus=1&page={}"

heads = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}


def get_players():
    for page in range(1, 11):
        code = requests.get(url.format(str(page)), headers=heads)
        content = code.content
        soup = BeautifulSoup(content, 'html.parser')
        players = soup.find_all("tr", class_=['even', 'odd'])
        for pl in players:
            name = pl.find_all('a')[0].get_text()
            prev_club = pl.find_all('a')[2]['title']
            cur_club = pl.find_all('a')[-3]['title']
            player = Player.objects.filter(name=name).first()
            prev_club_filter = Club.objects.filter(name=prev_club).first()
            cur_club_filter = Club.objects.filter(name=cur_club).first()
            if cur_club_filter:
                if prev_club_filter and player:
                    player.club_id = cur_club_filter.id
                    player.save()
            else:
                if prev_club_filter and player:
                    player.delete()

get_players()


