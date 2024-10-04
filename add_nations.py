import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import requests
from bs4 import BeautifulSoup
from fantasy.models import Nation, Confederation

host = "https://www.transfermarkt.com"
nations_url = 'https://www.transfermarkt.com/wettbewerbe/fifa?ajax=yw1&page={}'

heads = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

def get_nations():
    for page in range(1, 10):
        code = requests.get(nations_url.format(str(page)), headers=heads)
        soup = BeautifulSoup(code.content, 'html.parser')
        nations = soup.find_all("tr", class_=['even', 'odd'])
        for nation in nations:
            name = nation.find('a')['title']
            confederation = nation.find_all('td')[-2].get_text()
            url = host + nation.find('a')['href']
            code = requests.get(url, headers=heads)
            soup = BeautifulSoup(code.content, 'html.parser')
            flag = soup.find('img', class_='flaggenrahmen')['src']
            nat = Nation(name=name, confederation=Confederation.objects.filter(name=confederation).first(), url=url, flag_url=flag)
            nat.save()

get_nations()