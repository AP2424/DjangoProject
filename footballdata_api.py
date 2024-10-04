import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import requests
from fantasy.models import Team
from blog.models import FanClub

available_leagues = ['EC', 'CL', 'PL', 'PD', 'BL1', 'SA', 'PPL', 'FL1', 'CLI', 'ELC', 'WC']
leagues = ['EC', 'PL'] # for testing

BASE_URL = 'https://api.football-data.org/v4/'
headers = {'X-Auth-Token': '333e20ec19514f0e8fac6c8e4e856530'}

# extract teams in all leagues
for league in leagues:
    url = BASE_URL + 'competitions/' + league + '/teams'
    response = requests.get(url=url, headers=headers)
    for team in response.json()['teams']:
        print(team)
        team_new = Team(name=str(team['name']))
        team_new.save()
        fanclub = FanClub(team=team_new)
        fanclub.save()


# extract league standings
"""for league in leagues:
    url = BASE_URL + 'competitions/' + league + '/standings'
    response = requests.get(url=url, headers=headers)
    for team in response.json()['standings']:
        print(team)"""

# extract top scorers
"""def fetch_topscorers(league):
    url = BASE_URL + 'competitions/' + league + '/scorers'
    response = requests.get(url=url, headers=headers)
    for scorer in response.json()['scorers']:
        print(scorer)"""

# extract all league matches


# extract upcoming matches
"""def fetch_upcmatches():
    url = BASE_URL + '/matches'
    current_date = datetime.date.today()
    print(current_date)
    response = requests.get(url=url, headers=headers, params={'dateFrom': '2024-06-18', 'dateTo': '2024-06-20'})
    print(response.json())
    for match in response.json()['matches']:
        print(match)

fetch_upcmatches()

url = BASE_URL + '/persons/57301'
response = requests.get(url=url, headers=headers)
print(response.json())"""