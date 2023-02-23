from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, JobListing, JobApplication
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import jobportalapp.constants as jb_constants

# Create your views here.

@login_required(login_url='login')
def Home(request):
    return render(request, 'base.html')

def LoginPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_instance = User.objects.filter(email=email).last()
        if user_instance is None:
            messages.error(request,"Email id not registed....")
            return redirect('login')
        user = authenticate(username=user_instance.username, password=password)
        if user is None:
            messages.error(request,"Email or Password is Wrong....")
        else:
            user_profile_instance = UserProfile.objects.filter(user=user_instance).last()
            login(request, user)
            if user_profile_instance.role == jb_constants.EMPLOYER:
                employer_listings = JobListing.objects.filter(employer=user_instance)
                return redirect('employerdashboard')
            else:
                return redirect('seekerdashboard')
    return render(request, 'loginpage.html')

def RegisterPage(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']
        city = request.POST['city']
        role = request.POST['role']

        user_exists = User.objects.filter(Q(email=email) | Q(username=username)).exists()
        if user_exists:
            messages.info(request,"Username or Email Alredy Exists....")
            return redirect('register')
        else:
            user_instance = User.objects.create_user(username=username, password=password, email=email)
            user_profile = UserProfile.objects.create(
                user=user_instance,
                mobile = mobile,
                city = city,
                role = role
            )
            login(request, user_instance)
            if role == jb_constants.EMPLOYER:
                return redirect('employerdashboard')
            else:
                return redirect('seekerdashboard')
    return render(request, 'registerpage.html')

@login_required(login_url='login')
def LogoutView(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def EmployerDashboardView(request):
    job_listings = JobListing.objects.filter(employer=request.user)
    context = {
        'job_listings':job_listings
    }
    return render(request, 'employerdashboard.html', context=context)

@login_required(login_url='login')
def JobDetailPageView(request,id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        salary = request.POST['salary']
        location = request.POST['location']
        experience = request.POST['experience']

        job_instance = JobListing.objects.filter(id=id).last()

        job_instance.title = title
        job_instance.description = description
        job_instance.salary = salary
        job_instance.location = location
        job_instance.experience = experience

        job_instance.save()
        messages.success(request, "Job Details Edited successfully for "+job_instance.title)
        return redirect('employerdashboard')

    job_instance = JobListing.objects.filter(id=id).last()
    context = {
        'job_details':job_instance
    }
    return render(request, 'jobdetailspage.html', context=context)

@login_required(login_url='login')
def CreateJobView(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        salary = request.POST['salary']
        location = request.POST['location']
        experience = request.POST['experience']

        create_job_listing = JobListing.objects.create(
            employer = request.user,
            title = title,
            description = description,
            salary = salary,
            location = location,
            experience = experience
        )

        messages.success(request, 'Job Application Succussfully created for '+create_job_listing.title)
        return redirect('employerdashboard')

    return render(request, 'createjob.html')

@login_required(login_url='login')
def DeleteJobView(request,id):
    job_instance = JobListing.objects.filter(id=id).last()
    job_instance.delete()
    messages.success(request, job_instance.title + " job successfully deleted.")
    return redirect('employerdashboard')

@login_required(login_url='login')
def ApplicantView(request,id):
    if request.method == 'POST':
        job_seeker = request.POST['job_seeker']
        status = request.POST['status']
        job_list_instance = JobListing.objects.filter(id=id).last()
        job_seeker = User.objects.filter(id=job_seeker).last()
        job_applicant_instace = JobApplication.objects.filter(job=job_list_instance, job_seeker=job_seeker).last()
        job_applicant_instace.status = status
        job_applicant_instace.save()

        return redirect('employerdashboard') 

    job_listing_instance = JobListing.objects.filter(id=id).last()
    job_applicants = JobApplication.objects.filter(job=job_listing_instance)

    context ={
        'job_applicants':job_applicants
    }
    return render(request, 'applicantview.html', context)

@login_required(login_url='login')
def SeekerDashboardView(request):
    if request.method == "POST":
        search = request.POST['search']
        print("SEarch", search)
        job_listings = JobListing.objects.filter(Q(title__icontains=search) | 
            Q(description__icontains=search) | 
            Q(salary__icontains=search) |
            Q(location__icontains=search) |
            Q(experience__icontains=search)  
        )
        context = {
            'job_listings':job_listings
        }
        return render(request, 'jobseekerdashboard.html', context=context)

    job_listings = JobListing.objects.all()
    context = {
        'job_listings':job_listings
    } 
    return render(request, 'jobseekerdashboard.html', context=context)

@login_required(login_url='login')
def ViewJob(request, id):
    job_listing_instance = JobListing.objects.filter(id=id).last()
    context = {
        'job_details':job_listing_instance
    } 
    return render(request, 'viewjob.html', context=context)

@login_required(login_url='login')
def ApplyJob(request, id):
    if request.method == "POST":
        resume = request.FILES['resume']

        job_listing_instance = JobListing.objects.filter(id=id).last()
        apply_job = JobApplication.objects.create(
            job_seeker = request.user,
            job = job_listing_instance,
            status = "Pending",
            file= resume
        )
        messages.success(request, "Application sent successfully for "+ job_listing_instance.title)
        return redirect('seekerdashboard')

@login_required(login_url='login')
def AppliedJob(request):
    applied_jobs = JobApplication.objects.filter(job_seeker = request.user)
    context = {
        'applied_jobs' : applied_jobs
    }
    return render(request, 'appliedjobs.html', context=context)



    
