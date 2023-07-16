from django.db import models
from django.contrib.auth.models import User

from team.models import Team

class Lead(models.Model):
    LOW = 'low'
    HIGH = 'high'
    MEDIUM = 'medium'

    CHOICES_PRIORITY = (
        (LOW, 'low'),
        (HIGH, 'high'),
        (MEDIUM, 'medium'),
    )

    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'

    CHOICES_STATUS = (
        (NEW, 'new'),
        (CONTACTED, 'contacted'),
        (WON, 'won'),
        (LOST, 'lost'),
    )

    team = models.ForeignKey(Team, related_name='lead', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=NEW)
    priority = models.CharField(max_length=10,choices=CHOICES_PRIORITY, default=MEDIUM)
    converted_to_clients = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        

    def __str__(self):
        return self.name

class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='lead_comments', on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='leads_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True,null=True)
