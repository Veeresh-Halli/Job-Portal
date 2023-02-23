from django.urls import path
from . import views

urlpatterns = [
    path('home', views.Home, name='home'),
    path('login', views.LoginPage, name='login'),
    path('register', views.RegisterPage, name='register'),
    path('logout', views.LogoutView, name='logout'),
    #Employer related urls
    path('employer-dashboard', views.EmployerDashboardView, name='employerdashboard'),
    path('job-detail-page/<int:id>/', views.JobDetailPageView, name='job-details'),
    path('create-job/', views.CreateJobView, name='create-job'),
    path('delete-job/<int:id>/', views.DeleteJobView, name='delete-job'),
    path('view-applicants/<int:id>/', views.ApplicantView, name='applicant-view'),
    #Jobseeker related urls
    path('job-seeker-dashboard', views.SeekerDashboardView, name='seekerdashboard'),
    path('view-job/<int:id>/', views.ViewJob, name='view-job'),
    path('apply-job/<int:id>/', views.ApplyJob, name='apply-job'),
    path('applied-jobs/', views.AppliedJob, name='applied-jobs'),
]
