from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Team, TeamMemberRequest, TeamMember
from .forms import ApproveUserForm
@login_required
def create_team(request):
    if request.method == "POST":
        name = request.POST.get("team-name")
        description = request.POST.get("team-description")
        image = request.FILES.get("image")

        if not name:  # Validate required fields
            messages.error(request, "Team name is required.")
        else:
            # Create the team
            team = Team.objects.create(
                name=name,
                description=description,
                image=image,
                created_by=request.user
            )

            # Add the creator as an admin member
            TeamMember.objects.create(
                team=team,
                user=request.user,
                is_admin=True  # Set the creator as admin
            )

            messages.success(request, "Team created successfully!")
            return redirect(reverse("team_detail", kwargs={"team_id": team.id}))

    return render(request, "teams/create_team.html")

# Team Detail View
@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    # Fetch all members, checking the `is_admin` field instead of `role`
    team_members = TeamMember.objects.filter(team=team)

    context = {
        "team": team,
        "team_members": team_members,
    }
    return render(request, "teams/team_detail.html", context)



# List All Teams
@login_required
def list_teams(request):
    teams = Team.objects.all()
    teams_with_status = []

    for team in teams:
        is_member = TeamMember.objects.filter(user=request.user, team=team).exists()
        teams_with_status.append({'team': team, 'is_member': is_member})

    return render(request, 'teams/list_teams.html', {'teams': teams_with_status})


# Join Team Request
@login_required
def join_team_request(request, pk):
    team = get_object_or_404(Team, id=pk)
    is_member = TeamMember.objects.filter(user=request.user, team=team).exists()

    if request.method == 'POST':
        if is_member:
            messages.warning(request, "You are already a member of this team.")
            return redirect('list_teams')

        if TeamMemberRequest.objects.filter(user=request.user, team=team).exists():
            messages.warning(request, "You have already sent a join request for this team.")
            return redirect('list_teams')

        # Create a join request
        message = request.POST.get('message', '')
        TeamMemberRequest.objects.create(user=request.user, team=team, message=message)
        messages.success(request, "Your join request has been sent successfully.")
        return redirect('list_teams')

    return render(request, 'teams/join_team_request.html', {'team': team, 'is_member': is_member})


# Manage Join Requests (Admin Only)
@login_required
def manage_requests(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    is_admin = TeamMember.objects.filter(user=request.user, team=team, role="admin").exists()

    if not is_admin:
        messages.error(request, "You do not have permission to manage requests for this team.")
        return redirect("list_teams")

    join_requests = team.requests.filter(status="Pending")
    return render(request, "teams/manage_requests.html", {"team": team, "join_requests": join_requests})

# Approve Join Request
@login_required
def approve_request(request, request_id):
    # Get the join request
    join_request = get_object_or_404(TeamMemberRequest, id=request_id)

    # Check if the logged-in user is an admin of the team
    is_admin = TeamMember.objects.filter(team=join_request.team, user=request.user, is_admin=True).exists()
    if not is_admin:
        messages.error(request, "Only team admins can approve join requests.")
        return redirect('team_detail', team_id=join_request.team.id)

    # Add the user to the team
    TeamMember.objects.create(team=join_request.team, user=join_request.user)

    # Delete the join request
    join_request.delete()

    messages.success(request, f"{join_request.user.username} has been added to the team and the request was deleted.")

    return redirect('team_detail', team_id=join_request.team.id)

# Delete Team
@login_required
def delete_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == "POST" and request.user == team.created_by:
        team.delete()
        messages.success(request, "The team was deleted successfully.")
        return redirect("list_teams")
    return render(request, "teams/delete_team.html", {"team": team})


# View All Join Requests (Admin Dashboard)
@login_required
def view_requests(request):
    requests = JoinRequest.objects.all()
    return render(request, "teams/view_users_request.html", {"requests": requests})


