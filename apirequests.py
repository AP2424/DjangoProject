import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import requests

BASE_URL = 'http://localhost:8000/'

endpoints = ['competitions/', 'clubs/', 'players/']

competitions_ids = ['GB1', 'ES1', 'IT1', 'L1', 'FR1', 'TR1', 'PO1', 'NL1', 'BE1', 'A1', 'SC1', 'GR1']

for i in range(len(competitions_ids)):
    league_path = BASE_URL + endpoints[0] + competitions_ids[i]
    response = requests.get(league_path + '/clubs')
    league_data = response.json()
    print(league_data)
    clubs = league_data['clubs']
    for club in clubs:
        club_path = BASE_URL + endpoints[1] + club['id']
        club_profile = requests.get(club_path + '/profile').json()
        club_squad = requests.get(club_path + '/players').json()
        for player in club_squad['players']:
            print(player['name'])
            player_path = BASE_URL + endpoints[2] + player['id']
            player_profile = requests.get(player_path + '/profile')
            player_marketvalue = requests.get(player_path + '/market_value')
            player_transfers = requests.get(player_path + '/transfers')
            player_jerseynumbers = requests.get(player_path + '/jersey_numbers')
            player_stats = requests.get(player_path + '/stats')
            player_injuries = requests.get(player_path + '/injuries')
            player_achievements = requests.get(player_path + '/achievements')