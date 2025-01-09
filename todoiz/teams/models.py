from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_member(self, user):
        """Check if the given user is a member of the team."""
        return self.members.filter(user=user).exists()



class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)  # New field to indicate admin status
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "team")  # Prevent duplicate memberships

    def __str__(self):
        role = "Admin" if self.is_admin else "Member"
        return f"{self.user.username} ({role}) of {self.team.name}"


class TeamMemberRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=(("Pending", "Pending"), ("Accepted", "Accepted"), ("Rejected", "Rejected")),
        default="Pending"
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "team")  # Prevent duplicate requests

    def __str__(self):
        return f"{self.user.username} requested to join {self.team.name}"


