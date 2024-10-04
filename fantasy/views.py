from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Player, Team, League, UserTeam, Poll, Match
import search_algorithms as sl


def guide(request):
	return render(request, 'fantasy/guide.html')

def daily(request):
	polls = Poll.objects.all().order_by('-votes')
	polls1 = [polls[i] for i in range(0, len(polls), 2)]
	polls2 = [polls[i] for i in range(1, len(polls), 2)]
	print(polls[0])
	context = {'polls1': polls1, 'polls2': polls2}
	return render(request, 'fantasy/daily.html', context=context)

@login_required
def myteam(request):
	team = UserTeam.objects.filter(owner=request.user).first()
	if not team:
		return redirect('create-team')
	team_value = 0
	for player in team.players.all():
		team_value += player.value
	age = list(team.players.all().aggregate(Sum('age')).values())[0]
	if age:
		average_age = round(age/len(team.players.all()), 1)
	else:
		average_age = 0
	if request.method == 'POST' and team.completed == False:
		positions = [pl.position for pl in team.players.all()]
		goalies = positions.count('Goalkeeper')
		cbs = positions.count('Centre-Back')
		lbs = positions.count('Left-Back')
		rbs = positions.count('Right-Back')
		dms = positions.count('Defensive Midfield')
		cms = positions.count('Central Midfield')
		ams = positions.count('Attacking Midfield')
		rws = positions.count('Right Winger')
		lws = positions.count('Left Winger')
		cfs = positions.count('Centre-Forward')
		lms = positions.count('Left Midfield')
		rms = positions.count('Right Midfield')
		sss = positions.count('Second Striker')
		if len(team.players.all()) == 11 and goalies == 1 and cbs == 2 and lbs == 1 and rbs == 1 and dms == 1 and cms == 1 and ams == 1 and (rws == 1 or rms == 1) and (lws == 1 or lms == 1) and (cfs == 1 or sss == 1):
			if average_age <= 30.0:
				messages.success(request, 'You have finished setuping your fantasy team!')
				team.completed = True
				team.save()
			else:
				messages.warning(request, 'Your team is too old!')
		else:
			messages.warning(request, 'Some positions are filled wrong')
		return redirect('team')
	goalkeeper = team.players.filter(position="Goalkeeper").first()
	left_back = team.players.filter(position="Left-Back").first()
	left_centre_back = team.players.filter(position="Centre-Back").first()
	right_centre_back = team.players.filter(position="Centre-Back").last()
	if left_centre_back == right_centre_back:
		right_centre_back = None
	right_back = team.players.filter(position="Right-Back").first()
	defensive_midfield = team.players.filter(position="Defensive Midfield").first()
	central_midfield = team.players.filter(position="Central Midfield").first()
	attacking_midfield = team.players.filter(position="Attacking Midfield").first()
	left_winger = team.players.filter(position__in=["Left Winger", "Left Midfield"]).first()
	right_winger = team.players.filter(position__in=["Right Winger", "Right Midfield"]).first()
	centre_forward = team.players.filter(position__in=["Centre-Forward", "Second Striker"]).first()
	return render(request, 'fantasy/team.html', context={'team': team, 'players': team.players.order_by("number"), 'value': team_value, 'age': average_age, 'goalkeeper': goalkeeper, 'left_back': left_back, 'left_centre_back': left_centre_back, 'right_centre_back': right_centre_back, 'right_back': right_back, 'defensive_midfield': defensive_midfield, 'attacking_midfield': attacking_midfield, 'central_midfield': central_midfield, 'left_winger': left_winger, 'right_winger': right_winger, 'centre_forward': centre_forward})

def userteam(request, name):
	team = UserTeam.objects.filter(name=name).first()
	team_pts = [t.points for t in UserTeam.objects.all() if t.name != team.name]
	rank = 1
	last_equal = 1
	for pt in team_pts:
		if pt > team.points:
			rank += 1
			last_equal += 1
		elif pt == team.points:
			last_equal += 1
	if rank != last_equal:
		rank = f'{rank}-{last_equal}'
	return render(request, 'fantasy/userteam.html', context={'team': team})


class CreateTeamView(LoginRequiredMixin, CreateView):
	model = UserTeam
	fields = ['name', 'description', 'logo']
	template_name = 'fantasy/team_form.html'
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)

class LeagueListView(ListView):
	model = League
	paginate_by = 50
	context_object_name = 'leagues'
	def post(self, request, *args, **kwargs):
		if request.method == "POST":
			query = request.POST.get('query')
			return redirect('search', query=query)


class ClubListView(ListView):
	model = Team
	paginate_by = 50
	context_object_name = 'clubs'
	def get_queryset(self):
		league = get_object_or_404(League, name=self.kwargs.get('league'))
		return Team.objects.filter(league=league).order_by('place')
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		league = League.objects.filter(name=self.kwargs.get('league')).first()
		players = Player.objects.filter(club__league=league)
		scorers = players.order_by('-goals')[0:5]
		assisters = players.order_by('-assists')[0:5]
		exp_players = players.order_by('-value')[0:5]
		youngest = players.order_by('age')[0:5]
		oldest = players.order_by('-age')[0:5]
		yellows = players.order_by('yellow_cards')[0:5]
		reds = players.order_by('yellow_cards')[0:5]
		context['league'] = league
		context['scorers'] = scorers
		context['assisters'] = assisters
		context['exp_players'] = exp_players
		context['youngest'] = youngest
		context['oldest'] = oldest
		context['yellows'] = yellows
		context['reds'] = reds
		context['yellows'] = yellows
		return context

class ClubDetailedListView(ListView):
	model = Team
	paginate_by = 50
	template_name = 'fantasy/club_detailed_list.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		league = League.objects.filter(name=self.kwargs.get('league')).first()
		club = Team.objects.filter(league=league).order_by('place')
		clubs_num = int(len(Team.objects.filter(league=league)))
		last_survival_place = clubs_num - league.relegation_places
		champions_and_europa = league.champions_league_places + league.europa_league_places
		all_cups_places = league.champions_league_places + league.europa_league_places + league.conference_league_places
		places = [i for i in range(1, clubs_num + 1)]
		clubs = zip(club, places)
		context['league'] = league
		context['clubs'] = clubs
		context['last_survival_place'] = last_survival_place
		context['champions_europa'] = champions_and_europa
		context['all_cups_places'] = all_cups_places
		return context

class LeagueMatchesView(ListView):
	model = Match
	context_object_name = 'matches'
	template_name = 'fantasy/league_matches.html'
	def get_queryset(self):
		league = get_object_or_404(League, name=self.kwargs.get('league'))
		return Match.objects.filter(league=league).filter(type="PAST")
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		league = get_object_or_404(League, name=self.kwargs.get('league'))
		match_objects = Match.objects.filter(league=league).filter(type="PAST")
		matches_and_dates = sort_matches_by_dates(match_objects)
		context['league'] = league
		context['dates'] = matches_and_dates[0]
		context['matches'] = matches_and_dates[1]
		return context

class LeagueNextMatchdayView(ListView):
	model = Match
	template_name = 'fantasy/next_matchday.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		league = get_object_or_404(League, name=self.kwargs.get('league'))
		match_objects = Match.objects.filter(league=league).filter(type="NEXT")
		dates = []
		matches_by_date =[]
		for match in match_objects:
			if match.date not in dates:
				dates.append(match.date)
		dates.sort()
		for date in dates:
			match_set = match_objects.filter(date=date)
			matches_by_date.append(match_set)
		matches = zip(dates, matches_by_date)
		context['league'] = league
		context['dates'] = dates
		context['matches'] = matches
		return context

def sort_matches_by_dates(match_objects):
	dates = []
	matches_by_date = []
	for match in match_objects:
		if match.date not in dates:
			dates.append(match.date)
	dates.sort()
	for date in dates:
		match_set = match_objects.filter(date=date)
		matches_by_date.append(match_set)
	matches = zip(dates, matches_by_date)
	return dates, matches


class LeagueStatisticsView(ListView):
	model = Player
	template_name = 'fantasy/league_statistics.html'
	context_object_name = 'players'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		league = get_object_or_404(League, name=self.kwargs.get('league'))
		players = Player.objects.filter(club__league=league)
		scorer = players.order_by('-goals')[0:5]
		assister = players.order_by('-assists')[0:5]
		exp_player = players.order_by('-value')[0:5]
		youngest_player = players.order_by('age')[0:5]
		oldest_player = players.order_by('-age')[0:5]
		yellow = players.order_by('-yellow_cards')[0:5]
		red = players.order_by('-red_cards')[0:5]
		point = players.order_by('-points')[0:5]
		ranks = [i for i in range(1, 6)]
		exp_players = zip(exp_player, ranks)
		scorers = zip(scorer, ranks)
		assisters = zip(assister, ranks)
		youngest_players = zip(youngest_player, ranks)
		oldest_players = zip(oldest_player, ranks)
		yellows = zip(yellow, ranks)
		reds = zip(red, ranks)
		points = zip(point, ranks)
		context['league'] = league
		context['scorers'] = scorers
		context['assisters'] = assisters
		context['exp_players'] = exp_players
		context['youngest'] = youngest_players
		context['oldest'] = oldest_players
		context['yellows'] = yellows
		context['reds'] = reds
		context['points'] = points
		return context

class ClubStatsView(ListView):
	model = Player
	context_object_name = 'players'
	template_name = 'fantasy/club_stats.html'
	paginate_by = 50
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		club = get_object_or_404(Team, name=self.kwargs.get('club'))
		players = Player.objects.filter(club=club)
		scorers = players.order_by('-goals')[0:10]
		assisters = players.order_by('-assists')[0:10]
		exp_players = players.order_by('-value')[0:10]
		places = club.table_history.split()
		context['club'] = club
		context['scorers'] = scorers
		context['assisters'] = assisters
		context['exp_players'] = exp_players
		context['places'] = places
		return context

class ClubPlayerSquadView(ListView):
	model = Player
	context_object_name = 'players'
	template_name = 'fantasy/club_squad.html'
	def get_queryset(self):
		club = get_object_or_404(Team, name=self.kwargs.get('club'))
		return Player.objects.filter(club=club)
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		club = get_object_or_404(Team, name=self.kwargs.get('club'))
		players = Player.objects.filter(club=club)
		goalkeepers = players.filter(position='Goalkeeper').order_by('-value')
		defenders = players.filter(position__in=['Left-Back', 'Centre-Back', 'Right-Back']).order_by('-value')
		midfielders = players.filter(position__in=['Left Midfield', 'Defensive Midfield', 'Right Midfield', 'Attacking Midfield', 'Central Midfield']).order_by('-value')
		attackers = players.filter(position__in=['Left Winger', 'Right Winger', 'Centre-Forward', 'Second Striker']).order_by('-value')
		context['club'] = club
		context['goalkeepers'] = goalkeepers
		context['defenders'] = defenders
		context['midfielders'] = midfielders
		context['attackers'] = attackers

		return context

class ClubMatchesView(ListView):
	model = Match
	context_object_name = 'matches'
	template_name = 'fantasy/club_matches.html'
	def get_queryset(self):
		club = get_object_or_404(Team, name=self.kwargs.get('club'))
		return Match.objects.filter(home_club=club) | Match.objects.filter(away_club=club)
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		club = get_object_or_404(Team, name=self.kwargs.get('club'))
		context['club'] = club
		return context

class MatchView(DetailView):
	model = Match
	context_object_name = 'match'
	template_name = 'fantasy/match.html'


class PlayerDetailView(LoginRequiredMixin, DetailView):
	model = Player
	def get(self, request, *args, **kwargs):
		team = UserTeam.objects.filter(owner=request.user).first()
		team_value = list(team.players.all().aggregate(Sum('value')).values())[0]
		if team_value:
			available = 500.0 - team_value
		else:
			available = 500.0
		player = self.get_object()
		count = 0
		for t in UserTeam.objects.all():
			if player in t.players.all():
				count += 1
		player.popularity_number += 1
		player.save()
		return render(request, "fantasy/player_detail.html", context={'available': available, 'object': player, 'picked': count})

	def post(self, request, *args, **kwargs):
		if request.method == "POST":
			team = UserTeam.objects.filter(owner=request.user).first()
			team_value = list(team.players.all().aggregate(Sum('value')).values())[0]
			if team_value:
				available = 500.0 - team_value
			else:
				available = 500.0
			if not team:
				return redirect('create-team')
			player = self.get_object()
			if player in team.players.all():
				team.players.remove(player)
				messages.success(request, f'You have sold {player.name} for €{player.value} m!')
				return redirect('team')
			else:
				if available > player.value:
					team.players.add(player)
					messages.success(request, f'You have signed {player.name} for €{player.value} m')
					return redirect('club-squad', player.club.name)
				else:
					messages.warning(request, f"You haven't got enough money to sign {player.name}")


class TeamsListView(ListView):
	model = UserTeam
	context_object_name = 'teams'
	paginate_by = 50
	def get_queryset(self):
		return UserTeam.objects.filter(completed=True).order_by('-points')

class SearchView(ListView):
	model = Player
	context_object_name = 'players'
	template_name = 'fantasy/search.html'
	paginate_by = 10
	def get_queryset(self):
		matched_players = []
		query = self.kwargs.get('query')
		for letter in query:
			if letter in sl.keyboard_ru_en.keys():
				modquery = query.replace(letter, sl.keyboard_ru_en[letter])
				query = modquery
		for player in Player.objects.all():
			if query.lower() in player.name.lower():
				matched_players.append(player)
		def popularity(player):
			return player.popularity_number
		matched_players.sort(reverse=True, key=popularity)
		return matched_players

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		query = self.kwargs.get('query')
		context['query'] = query
		return context






	



