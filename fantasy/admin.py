from django.contrib import admin
from .models import Player, Team, League, UserTeam, Tactic, Nation, \
    Poll, PollChoice, Match, Referee, Coach


admin.site.register(Player)
admin.site.register(Referee)
admin.site.register(Coach)
admin.site.register(Team)
admin.site.register(League)
admin.site.register(UserTeam)
admin.site.register(Tactic)
admin.site.register(Nation)
admin.site.register(Poll)
admin.site.register(PollChoice)
admin.site.register(Match)








