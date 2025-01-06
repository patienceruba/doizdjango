from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name="created_teams")
    members = models.ManyToManyField(User, related_name="teams", through="TeamMembership" )
    image = models.ImageField(upload_to='images/')


    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "team")  # Prevent duplicate memberships

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"


class JoinRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="join_requests"
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="join_requests"
    )
    message = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    #notification_sent = models.BooleanField(default=False)  # For future notifications

    class Meta:
        unique_together = ("user", "team")  # Prevent duplicate requests

    def __str__(self):
        status = "Approved" if self.is_approved else "Pending"
        return f"JoinRequest: {self.user.username} -> {self.team.name} ({status})"
