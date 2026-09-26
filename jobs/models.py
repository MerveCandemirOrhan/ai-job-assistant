from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    ai_analysis = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title

class CV(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
)
    file = models.FileField(upload_to="cvs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ai_analysis = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name 