from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Team, JoinRequest
from django.contrib import messages
from .models import Team


@login_required
def list_teams(request):
    teams = Team.objects.all()
    return render(request, 'teams/list_teams.html', {'teams': teams})

@login_required
def join_team_request(request, pk):
    team = get_object_or_404(Team, id=pk)
    if request.method == 'POST':
        JoinRequest.objects.create(user=request.user, team=team, message=request.POST.get('message', ''))
        return redirect('list_teams')
    return render(request, 'teams/join_team_request.html', {'team': team})



@login_required
def manage_requests(request, team_id):
    """
    Displays a list of join requests for the specified team.
    """
    team = get_object_or_404(Team, id=team_id, created_by=request.user)
    join_requests = JoinRequest.objects.filter(team=team, is_approved=False)

    return render(request, 'teams/manage_requests.html', {'join_requests': join_requests, 'team': team})




@login_required
def approve_request(request, pk):
    """
    Approves a join request for a team and adds the user to the team.

    This view checks if the logged-in user is the team creator,
    approves the request, and adds the user to the team's members.
    """
    # Retrieve the join request object or return a 404 if not found
    join_request = get_object_or_404(
        JoinRequest, 
        id=pk, 
        team__created_by=request.user  # Ensure only the team creator can approve
    )
    
    # Approve the join request
    join_request.is_approved = True
    join_request.save()

    # Add the user to the team members
    join_request.team.members.add(join_request.user)

    # Redirect to the manage requests page
    return redirect('manage_requests', team_id=join_request.team.id)



@login_required
def create_team(request):
    join_request = get_object_or_404(JoinRequest, id=pk, team__created_by=request.user)
    join_request.is_approved = True
    join_request.save()
    join_request.team.members.add(join_request.user)
    return redirect('manage_requests', team_id=join_request.team.id)


from django.urls import reverse


@login_required
def create_team(request):
    if request.method == "POST":
        name = request.POST.get("team-name")
        description = request.POST.get("team-description")
        image = request.FILES.get('image') 
        if not name:  # Validate required fields
            messages.error(request, "Team name is required.")
        else:
            team = Team.objects.create(
                name=name,
                description=description,
                created_by=request.user,
                image=image
            )
            team.members.add(request.user)  # Automatically add the creator as a member
            messages.success(request, "Team created successfully!")
            
            # Redirect to the team's detail page using reverse
            return redirect(reverse('team', kwargs={'team_id': team.id}))

    return render(request, "teams/create_team.html")


from django.shortcuts import render, get_object_or_404

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, "teams/team_detail.html", {'team': team})


def deleteTeam(request, pk):
    item = get_object_or_404(Team, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "The team was deleted successfully.")
        return redirect("home")  # Replace "home" with the name of the view or URL to redirect to after deletion
    return render(request, "teams/deleteteam.html", {"item": item})