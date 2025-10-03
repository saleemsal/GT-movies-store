from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    suggested_movie_title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def yes_count(self):
        return self.votes.count()

class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petition_votes')
    voted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('petition', 'voter')  # one vote per user per petition

    def __str__(self):
        return f"{self.voter} → {self.petition}"
