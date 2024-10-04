from django.urls import path
from .views import guide, myteam, userteam, daily, LeagueListView, LeagueMatchesView, LeagueStatisticsView,\
    PlayerDetailView, ClubStatsView, ClubPlayerSquadView, ClubMatchesView, ClubListView, CreateTeamView,\
    TeamsListView, ClubDetailedListView, MatchView, LeagueNextMatchdayView, SearchView

urlpatterns = [
    path('', LeagueListView.as_view(), name='fantasy'),
    path('daily', daily, name='daily'),
    path('guide/', guide, name='guide'),
    path('team/create', CreateTeamView.as_view(), name='create-team'),
    path('myteam/', myteam, name='team'),
    path('team/<str:name>', userteam, name='userteam'),
    path('league/<str:league>/compact-table', ClubListView.as_view(), name='clubs'),
    path('league/<str:league>/detailed-table', ClubDetailedListView.as_view(), name='clubs-det'),
    path('league/<str:league>/matches', LeagueMatchesView.as_view(), name='league-matches'),
    path('league/<str:league>/next-matchday', LeagueNextMatchdayView.as_view(), name='league-next-matchday'),
    path('league/<str:league>/statistics', LeagueStatisticsView.as_view(), name='league-statistics'),
    path('club/<str:club>/stats', ClubStatsView.as_view(), name='club-stats'),
    path('club/<str:club>/squad', ClubPlayerSquadView.as_view(), name='club-squad'),
    path('club/<str:club>/matches', ClubMatchesView.as_view(), name='club-matches'),
    path('match/<int:pk>/', MatchView.as_view(), name='match'),
    path('player/<int:pk>/', PlayerDetailView.as_view(), name='player-detail'),
    path('leaderboard/', TeamsListView.as_view(), name='leaderboard'),
    path('search/<str:query>/', SearchView.as_view(), name='search')
]