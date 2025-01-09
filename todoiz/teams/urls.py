from django.urls import path
from . import views

'''urlpatterns = [
    path('teams/', views.list_teams, name='list_teams'),
    path('teams/<int:pk>/join/', views.join_team_request, name='join_team_request'),
   # URL pattern to manage join requests for a specific team
    path('team/<int:team_id>/manage-requests/', views.manage_requests, name='manage_requests'),

   #path('requests/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    path("teams/create/", views.create_team, name="create_team"),
    path('create/', views.create_team, name='create_team'),
    path('<int:team_id>/', views.team_detail, name='team'),  # This handles viewing the team detail
 # URL pattern for approving a join request
   # path('teamrequests/<int:pk>/approve/', views.approve_request, name='approve_request'),

    # Assuming you have a view to manage requests
    path('team/<int:pk>/manage-requests/', views.manage_requests, name='manage_requests'),
   path("deleteteam/<str:pk>/", views.delete_team, name="deleteteam"),

   path('approve_user/', views.approve_user_view, name='approve_user'),
   path("viewRequest", views. view_Request, name="viewRequest" )
]


from django.urls import path
from . import views
'''
urlpatterns = [
    # Teams
    path('teams/', views.list_teams, name='list_teams'),
    path('teams/create/', views.create_team, name='create_team'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('teams/<int:pk>/join/', views.join_team_request, name='join_team_request'),
    path('teams/<int:pk>/delete/', views.delete_team, name='delete_team'),
    
    # Manage Requests
    path('teams/<int:team_id>/requests/', views.manage_requests, name='manage_requests'),
    path('requests/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    
    # Admin Dashboard
    path('admin/requests/', views.view_requests, name='view_requests'),
]
