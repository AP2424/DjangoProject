import os
import django
from minutes_list import minutes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

import requests
from bs4 import BeautifulSoup
from fantasy.models import Player, Club, League, Team, Goal, Substitution, Card, Match
import datetime

host = "https://www.transfermarkt.com"

heads = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}



def get_html(link):
    code = requests.get(link, headers=heads)
    return code.content

def get_match_parameters(url):
    content = get_html(url)
    soup = BeautifulSoup(content, 'html.parser')
    matchday = soup.find('div', class_="sb-spieldaten").find('a').get_text()[0:-10]
    date = soup.find('div', class_="sb-spieldaten").find_all('a')[1].get_text().strip()
    year = int("20" + date[-2:])
    month = int(date[5])
    day = int(date[7:-3])
    date_obj = datetime.date(year, month, day)
    t = str(soup.find('p', class_="sb-datum").get_text())
    time = t.replace(" ", "")[-6:]
    if not '/' in time:
        hours = int(time[0])
        minutes = int(time[2:4])
        if "PM" in time:
            hours += 12
        time_obj = datetime.time(hours, minutes)
    else:
        time_obj = ''
    return date_obj, time_obj, matchday


def get_results(id, leagues):
    match_objects_list = []
    for obj in League.objects.filter(name__in=leagues):
        content = get_html(obj.url)
        soup = BeautifulSoup(content, 'html.parser')
        for i in range(2):
            matches = soup.find('div', id=id[i]).find_all('tr', class_='begegnungZeile')
            for match in matches:
                hometeam = match.find('td', class_='verein-heim').find('a')['title']
                awayteam = match.find('td', class_='verein-gast').find('a')['title']
                home_obj = Club.objects.filter(name=hometeam).first()
                away_obj = Club.objects.filter(name=awayteam).first()
                link = match.find('span', class_='ergebnis').find('a')
                if link:
                   url = host + link['href']
                result = match.find('span', class_=['matchresult finished', 'matchresult finished noSheet', 'matchresult']).get_text()
                if url and not "live" in url:
                    if not any(char.isalpha() for char in result) and not '-' in result:
                        ht_goals = int(result[0])
                        at_goals = int(result[2])
                        params = get_match_parameters(url)
                        match_obj = Match(type='PAST', league=obj, home_club=home_obj, away_club=away_obj,
                                  home_goals = ht_goals, away_goals = at_goals,
                                  date=params[0], time=params[1], matchday=params[2], url=url)
                        match_obj.save()
                        match_objects_list.append(match_obj)
                    else:
                        params = get_match_parameters(url)
                        match_obj = Match(type='NEXT', league=obj, home_club=home_obj, away_club=away_obj,
                              date=params[0], time=params[1], matchday=params[2], url=url)
                        match_obj.save()
    return match_objects_list


def main(id, leagues):
    for match in get_results(id, leagues):
        home = Club.objects.filter(name=match.home_club).first()
        away = Club.objects.filter(name=match.away_club).first()
        if match.home_goals > match.away_goals:
            home.points += 3
            home.wins += 1
            away.losses += 1
            home.save()
        elif match.home_goals < match.away_goals:
            away.points += 3
            away.wins += 1
            home.losses += 1
            away.save()
        elif match.home_goals == match.away_goals:
            home.points += 1
            away.points += 1
            home.draws += 1
            away.draws += 1
            home.save()
            away.save()
        home.scored += match.home_goals
        home.conceded += match.away_goals
        away.scored += match.away_goals
        away.conceded += match.home_goals
        home.save()
        away.save()
        content = get_html(match.url)
        soup = BeautifulSoup(content, 'html.parser')
        #check_goals_and_assists(match, soup)
        #check_cards(match, soup)
        #check_lineups(match, soup)
        #check_subs(match, soup)
    update_table()
    #update_fantasy_table()

def update_table():
    for league in League.objects.all():
        rated_clubs = []
        for club in Club.objects.filter(league=league):
            old_place = club.place
            club.place = 1
            for rc in rated_clubs:
                if rc.points > club.points:
                    club.place += 1
                elif rc.points < club.points:
                    rc.place += 1
                    rc.place_change -= 1
                elif rc.points == club.points:
                    if club.scored - club.conceded > rc.scored - rc.conceded:
                        rc.place += 1
                        rc.place_change -= 1
                    elif club.scored - club.conceded < rc.scored - rc.conceded:
                        club.place += 1
                    elif club.scored - club.conceded == rc.scored - rc.conceded:
                        if club.scored > rc.scored:
                            rc.place += 1
                            rc.place_change -= 1
                        elif club.scored < rc.scored:
                            club.place += 1
                        else:
                            club.place += 1
                rc.save()
            club.place_change = old_place - club.place
            club.table_history += str(club.place) + " "
            rated_clubs.append(club)
            club.save()

def update_fantasy_table():
    rated_teams = []
    for team in Team.objects.all():
        team.rank = 1
        for rt in rated_teams:
            if rt.points > team.points:
                team.rank += 1
            elif rt.points < team.points:
                rt.rank += 1
            rt.save()
        rated_teams.append(team)
        team.save()

def check_goals_and_assists(match, soup):
    goalsheet = soup.find('div', class_='sb-ereignisse', id='sb-tore')
    if goalsheet:
        goals = goalsheet.find_all('li', class_=['sb-aktion-heim', 'sb-aktion-gast'])
        for goal in goals:
            scorer = goal.find('div', class_='sb-aktion-aktion').find('a')['title']
            assister = goal.find('div', class_='sb-aktion-aktion').find_all('a')[-1]['title']
            minute_pos = goal.find('div', class_="sb-aktion-uhr").find('span')['style']
            minute = minutes.get(minute_pos)
            playerg = Player.objects.filter(name=scorer).first()
            playeras = Player.objects.filter(name=assister).first()
            if playerg:
                goalkoff = calculate_goalcoff(playerg)
                playerg.goals += 1
                playerg.points += goalkoff
                playerg.save()
                goal_obj = Goal(scorer=playerg, minute=minute, type='normal')
                goal_obj.save()
            if playerg and playeras and playerg != playeras:
                goal_obj.assister = playeras
                goal_obj.save()
                asscoff = calculate_asscoff(playeras)
                playeras.assists += 1
                playeras.points += asscoff
                playeras.save()
                match.goals.add(goal_obj)
    match.save()

def check_lineups(match, soup):
    content = get_html(host + soup.find('li', id='line-ups').find('a')['href'])
    soup2 = BeautifulSoup(content, 'html.parser')
    for i in range(4):
      lineup = soup2.find_all('div', class_='large-6 columns')[i]
      players = lineup.find_all('a', class_='wichtig')
      for pl in players:
          name = pl['title']
          player = Player.objects.filter(name=name).first()
          if player:
              if i == 0:
                  match.home_squad.add(player)
                  player.matches += 1
                  player.points += 10
                  player.save()
              elif i == 1:
                  match.away_squad.add(player)
                  player.matches += 1
                  player.points += 10
                  player.save()
              elif i == 2:
                  match.home_subs.add(player)
              else:
                  match.away_subs.add(player)
    match.save()

def check_subs(match, soup):
    subsheet = soup.find('div', class_='sb-ereignisse', id='sb-wechsel')
    if subsheet:
        subs = subsheet.find_all('li', class_=['sb-aktion-heim', 'sb-aktion-gast'])
        for sub in subs:
            sub_on = sub.find('span', class_='sb-aktion-wechsel-ein').find('a')['title']
            sub_off = sub.find('span', class_='sb-aktion-wechsel-aus').find('a')['title']
            minute_pos = sub.find('div', class_="sb-aktion-uhr").find('span')['style']
            minute = minutes.get(minute_pos)
            player_on = Player.objects.filter(name=sub_on).first()
            player_off = Player.objects.filter(name=sub_off).first()
            if player_on:
                player_on.matches += 1
                player_on.points += 5
                player_on.save()
            if player_off:
                player_off.points -= 3
                player_off.save()
            if player_off and player_on:
                sub_obj = Substitution(player_off=player_off, player_on=player_on, minute=minute, type='tactical')
                sub_obj.save()
                match.subs.add(sub_obj)
    match.save()

def check_cards(match, soup):
    cardsheet = soup.find('div', class_='sb-ereignisse', id='sb-karten')
    if cardsheet:
        cards = cardsheet.find_all('li', class_=['sb-aktion-heim', 'sb-aktion-gast'])
        for card in cards:
            violator = card.find('div', class_='sb-aktion-aktion').find('a')['title']
            type_text = card.find('div', class_='sb-aktion-aktion').get_text()
            player = Player.objects.filter(name=violator).first()
            minute_pos = card.find('div', class_="sb-aktion-uhr").find('span')['style']
            minute = minutes.get(minute_pos)
            type = ''
            if player:
                if "Red card" in type_text:
                    player.red_cards += 1
                    player.points -= 5
                    type = "Red card"
                elif "Yellow card" in type_text:
                    player.yellow_cards += 1
                    player.points -= 1
                    type = "Yellow card"
                elif "Second yellow" in type_text:
                    player.second_yellow_cards += 1
                    player.points -= 3
                    type = "Second yellow"
                player.save()
                card = Card(player=player, minute=minute, card=type)
                card.save()
                match.cards.add(card)
    match.save()

def calculate_goalcoff(player):
    goalcoff = 0
    if player.position in 'Goalkeeper':
        goalcoff = 50
    if player.position in ('Centre-Back', 'Left-Back', 'Right-Back'):
        goalcoff = 25
    elif player.position in ('Central Midfield', 'Defensive Midfield'):
        goalcoff = 20
    elif player.position in ('Left Midfield', 'Right Midfield', 'Attacking Midfield'):
        goalcoff = 15
    elif player.position in ('Left Winger', 'Right Winger', 'Second Striker'):
        goalcoff = 10
    elif player.position in 'Centre-Forward':
        goalcoff = 5
    return goalcoff

def calculate_asscoff(player):
    asscoff = 0
    if player.position in 'Goalkeeper':
        asscoff = 50
    if player.position in 'Centre-Back':
        asscoff = 25
    if player.position in ('Central Midfield', 'Defensive Midfield'):
        asscoff = 20
    elif player.position in ('Left Midfield', 'Right Midfield', 'Attacking Midfield', 'Left-Back', 'Right-Back'):
        asscoff = 15
    elif player.position in ('Left Winger', 'Right Winger', 'Second Striker', 'Centre-Forward'):
        asscoff = 10
    return asscoff

main(['spieltagtabs-1', 'spieltagtabs-2'], ['LaLiga', 'Serie A', 'Ligue 1', 'Bundesliga', 'Super Lig', 'Liga Portugal', 'Eredevisie'])