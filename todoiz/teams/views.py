from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Team, TeamMemberRequest, TeamMember
from .forms import ApproveUserForm
from django.http import JsonResponse

from django.http import HttpResponseForbidden


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
def team_detail(request, team_id):
    team = Team.objects.get(id=team_id)
    join_requests = TeamMemberRequest.objects.filter(team=team, status='Pending')
    
    return render(request, 'teams/team_detail.html', {
        'team': team,
        'join_requests': join_requests
    })




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
    team_request = get_object_or_404(TeamMemberRequest, id=request_id)

    if request.user == team_request.team.created_by or request.user == team_request.user:
        # Approve the request
        team_request.status = "Accepted"
        team_request.save()

        # Add user to the team as a member
        TeamMember.objects.create(
            team=team_request.team,
            user=team_request.user,
            is_admin=False,  # You can change this if needed
        )

        # Delete the request
        team_request.delete()

        return JsonResponse({'success': True, 'message': 'Request approved!', 'username': team_request.user.username, 'status': 'Accepted'})

    return JsonResponse({'success': False, 'message': 'Permission denied!'})


# reject 
def reject_request(request, id):
    # Get the request object by ID
    join_request = TeamMemberRequest.objects.get(id=id)
    # Change the status to 'Rejected'
    join_request.status = 'Rejected'
    join_request.save()

    # Redirect back to the team detail page
    return redirect('team_detail', team_id=join_request.team.id)


@login_required
def reject_request(request, request_id):
    team_request = get_object_or_404(TeamMemberRequest, id=request_id)

    if request.user == team_request.team.created_by or request.user == team_request.user:
        # Reject the request
        team_request.status = "Rejected"
        team_request.save()

        return JsonResponse({'success': True, 'message': 'Request rejected!', 'username': team_request.user.username, 'status': 'Rejected'})

    return JsonResponse({'success': False, 'message': 'Permission denied!'})


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



@login_required
def remove_member(request, team_id, member_id):
    team = get_object_or_404(Team, id=team_id)
    member = get_object_or_404(TeamMember, id=member_id, team=team)

    # Check if the current user is an admin of the team
    if not TeamMember.objects.filter(team=team, user=request.user, is_admin=True).exists():
        return HttpResponseForbidden("You are not allowed to perform this action.")

    # Prevent admins from removing themselves
    if member.user == request.user:
        return HttpResponseForbidden("Admins cannot remove themselves.")

    # Remove the member
    member.delete()
    return redirect("team_detail", team_id=team.id)
