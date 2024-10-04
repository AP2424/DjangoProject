from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import int_list_validator
import datetime


class Minute(models.Model):
    minute = models.IntegerField(default=0)

class Confederation(models.Model):
    name = models.CharField(max_length=50, default='', unique=True)

    def __str__(self):
        return self.name

class Nation(models.Model):
    name = models.CharField(max_length=50, default='', unique=True)
    confederation = models.ForeignKey(Confederation, default='', on_delete=models.CASCADE, null=True)
    flag_url = models.URLField(default='')
    url = models.URLField(default='')

    def __str__(self):
        return self.name


class Stadium(models.Model):
    name = models.CharField(max_length=50, default='')
    location = models.CharField(max_length=50, default='')
    capacity = models.IntegerField(default=0)
    yearOpened = models.SmallIntegerField(default=0)


class Team(models.Model):
    name = models.CharField(max_length=50)
    points = models.SmallIntegerField(default=0)
    int_points = models.SmallIntegerField(default=0)
    place = models.SmallIntegerField(default=0)
    place_change = models.SmallIntegerField(default=0)
    logo_url = models.URLField(default='', blank=True)

    def __str__(self):
        return self.name

class ClubTeam(Team):
    city = models.CharField(max_length=50, default='')
    table_history = models.CharField(max_length=100, default='', null=True, blank=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, null=True)

class NationalTeam(Team):
    confederation = models.ForeignKey(Confederation, on_delete=models.CASCADE)
    fifaRank = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

class Competition(models.Model):
    name = models.CharField(max_length=50, unique=False)
    participants = models.ManyToManyField(Team)
    logo = models.URLField(default='')

class League(Competition):
    nation = models.ForeignKey(Nation, default='', on_delete=models.CASCADE, null=True)
    relegation_places = models.SmallIntegerField(default=0)
    champions_league_places = models.SmallIntegerField(default=0)
    europa_league_places = models.SmallIntegerField(default=0)
    conference_league_places = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

class Person(models.Model):
    apiID = models.IntegerField(default=0)
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    birthdate = models.DateField()
    nationality = models.ForeignKey(Nation, default='', on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True


class Player(Person):
    image_url = models.URLField(default='')
    club = models.ForeignKey(Team, on_delete=models.CASCADE, default='', unique=False)
    position = models.CharField(max_length=30)
    value = models.FloatField()
    shirtNumber = models.SmallIntegerField(default=0)
    matches = models.SmallIntegerField(default=0)
    goals = models.SmallIntegerField(default=0)
    assists = models.SmallIntegerField(default=0)
    yellow_cards = models.SmallIntegerField(default=0)
    second_yellow_cards = models.SmallIntegerField(default=0)
    red_cards = models.SmallIntegerField(default=0)
    points = models.SmallIntegerField(default=0)
    popularity_number = models.FloatField(default=0)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'

class Coach(Person):
    image = models.ImageField(default='default.jpg')
    club = models.ForeignKey(Team, on_delete=models.CASCADE, default='', unique=False)

class Referee(Person):
    pass

class Goal(models.Model):
    scorer = models.ForeignKey(Player, default='', on_delete=models.CASCADE, related_name='scorer')
    assister = models.ForeignKey(Player, default='', on_delete=models.CASCADE, related_name='assister', null=True)
    minute = models.SmallIntegerField(default=0)
    type = models.CharField(max_length=50, default='')

    def __str__(self):
        return f'{self.scorer} ({self.minute})'

class Substitution(models.Model):
    player_off = models.ForeignKey(Player, default='', on_delete=models.CASCADE, related_name='player_off')
    player_on = models.ForeignKey(Player, default='', on_delete=models.CASCADE, related_name='player_on')
    minute = models.SmallIntegerField(default=0)
    type = models.CharField(max_length=50, default='')

    def __str__(self):
        return f'{self.player_on} for {self.player_off}, ({self.minute})'

class Card(models.Model):
    player = models.ForeignKey(Player, default='', on_delete=models.CASCADE)
    minute = models.SmallIntegerField(default=0)
    card = models.CharField(max_length=50, default='')

    def __str__(self):
        return f'{self.player}, {self.minute}'

class Match(models.Model):
    TYPES = [
        ('PAST', 'Past'),
        ('NEXT', 'Next')
    ]
    type = models.CharField(max_length=10, choices=TYPES, default='')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=True)
    matchday = models.SmallIntegerField(default=0)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    home_club = models.ForeignKey(Team, on_delete=models.CASCADE, unique=False, related_name="home")
    away_club = models.ForeignKey(Team, on_delete=models.CASCADE, unique=False, related_name="away")
    home_squad = models.ManyToManyField(Player, default='', related_name="home_squad")
    away_squad = models.ManyToManyField(Player, default='', related_name="away_squad")
    home_subs = models.ManyToManyField(Player, default='', related_name="home_subs")
    away_subs = models.ManyToManyField(Player, default='', related_name="away_subs")
    home_goals = models.SmallIntegerField(default=0)
    away_goals = models.SmallIntegerField(default=0)
    goals = models.ManyToManyField(Goal, default='')
    subs = models.ManyToManyField(Substitution, default='')
    cards = models.ManyToManyField(Card, default='')
    url = models.URLField(default='')

    def __str__(self):
        match = f"{self.home_club} - {self.away_club}"
        return match

class UserTeam(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    owner = models.OneToOneField(User, default='', on_delete=models.CASCADE)
    logo = models.ForeignKey(Team, default='', on_delete=models.CASCADE, null=True)
    players = models.ManyToManyField(Player)
    points = models.BigIntegerField(default=0)
    rank = models.SmallIntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team')

class Tactic(models.Model):
    name = models.CharField(max_length=50)
    cbs = models.SmallIntegerField(default=0)
    lbs = models.SmallIntegerField(default=0)
    rbs = models.SmallIntegerField(default=0)
    dms = models.SmallIntegerField(default=0)
    cms = models.SmallIntegerField(default=0)
    ams = models.SmallIntegerField(default=0)
    lws = models.SmallIntegerField(default=0)
    rws = models.SmallIntegerField(default=0)
    cfs = models.SmallIntegerField(default=0)

class PollChoice(models.Model):
    text = models.CharField(default='', max_length=50)
    image_url = models.URLField(default='')
    choiceid = models.SmallIntegerField(default=0)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text

CHOICES = [
    ('POLL', 'Poll'),
    ('QUIZ', 'Quiz')
]

class Poll(models.Model):
    title = models.CharField(default='', max_length=100)
    type = models.CharField(max_length=20, choices=CHOICES, default='')
    choices = models.ManyToManyField(PollChoice)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title





