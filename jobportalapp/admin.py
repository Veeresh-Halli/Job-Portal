from django.contrib import admin
from jobportalapp.models import UserProfile, JobListing, JobApplication

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(JobListing)
admin.site.register(JobApplication)