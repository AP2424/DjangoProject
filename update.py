import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import requests
from bs4 import BeautifulSoup
from fantasy.models import Player, Club, Nation

host = "https://www.transfermarkt.com"

heads = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

def get_html(link):
    code = requests.get(link, headers=heads)
    return code.content

def get_players():
    list = []
    all_clubs = Club.objects.all()
    club_id = Club.objects.first().id
    for club in all_clubs:
        content = get_html(club.url)
        soup = BeautifulSoup(content, 'html.parser')
        club.logo_url = soup.find('div', class_='data-header__profile-container').find('img')['src']
        club.save()
        players = soup.find_all("tr", class_=['even', 'odd'])
        for pl in players:
            try:
                name = pl.find_all('a')[-2].get_text().strip()
            except IndexError:
                print("Banned player")
            bdate = pl.find_all('td', class_='zentriert')[1].get_text()
            position = pl.find_all('td')[4].get_text()
            if not '-' in bdate:
                age = int(bdate[-3:-1])
                birthdate = bdate[0:-5]
            else:
                age = 0
            num = pl.find('div').get_text()
            if num != '-':
                number = int(num)
            else:
                number = 0
            nation = Nation.objects.filter(name=pl.find_all('img', class_ = 'flaggenrahmen')[0]['title']).first()
            value = pl.find_all('a')[-1].get_text()
            if any(char.isdigit() for char in value):
                if 'm' in value:
                    float_value = value[1:-1]
                elif 'Th' in value:
                    float_value = float(value[1:-3])/1000
                if not '-' in bdate:
                    db_object = Player.objects.filter(name=name).first()
                    if db_object:
                        db_object.age = age
                        db_object.birthdate = birthdate
                        db_object.position = position
                        db_object.club_id = club_id
                        db_object.value = float_value
                        db_object.nation = nation
                        db_object.number = number
                        db_object.save()
                    else:
                        link = pl.find_all('a')[-2]['href']
                        content = get_html(host + link)
                        soup = BeautifulSoup(content, 'html.parser')
                        image = soup.find('img', class_="data-header__profile-image")['src']
                        print(name)
                        list.append([name,
                                age,
                                birthdate,
                                club_id,
                                position,
                                number,
                                nation,
                                float_value,
                                image])
        club_id += 1
    return list

list = get_players()
for player in list:
    pl = Player(name=player[0], age=player[1], birthdate=player[2], club_id=player[3], position=player[4],
                number=player[5], nation=player[6], value=player[7], image_url=player[8])
    pl.save()