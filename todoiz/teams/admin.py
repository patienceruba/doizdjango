from django.contrib import admin
from .models import Team, TeamMembership, JoinRequest



admin.site.register(Team)
admin.site.register(TeamMembership)
admin.site.register(JoinRequest)