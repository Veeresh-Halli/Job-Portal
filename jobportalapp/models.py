from django.db import models
import jobportalapp.constants as jb_constants
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    role = models.CharField(choices=jb_constants.ROLES, max_length=10, default=jb_constants.EMPLOYER)

    def __str__(self):
        return self.user.username + " & Role" + self.role

class JobListing(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=25, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=25, null=True, blank=True)
    salary = models.CharField(max_length=10, null=True, blank=True)
    experience = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.title
       
class JobApplication(models.Model):
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    status = models.CharField(max_length=250, null=True, blank=True)
    file = models.FileField(upload_to='media')

    def __str__(self):
        return self.job_seeker.username + " " + self.job.title + " " + self.status
