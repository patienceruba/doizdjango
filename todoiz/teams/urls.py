from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.list_teams, name='list_teams'),
    path('teams/<int:team_id>/join/', views.join_team_request, name='join_team_request'),
   # URL pattern to manage join requests for a specific team
    path('team/<int:team_id>/manage-requests/', views.manage_requests, name='manage_requests'),

    path('requests/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    path("teams/create/", views.create_team, name="create_team"),
    path('create/', views.create_team, name='create_team'),
    path('<int:team_id>/', views.team_detail, name='team'),  # This handles viewing the team detail
 # URL pattern for approving a join request
    path('teamrequests/<int:pk>/approve/', views.approve_request, name='approve_request'),

    # Assuming you have a view to manage requests
    path('team/<int:team_id>/manage-requests/', views.manage_requests, name='manage_requests'),
   path("deleteteam/<str:pk>/", views.deleteTeam, name="deleteteam")
]
