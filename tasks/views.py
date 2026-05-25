from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task 

@login_required
def index(request):
    tasks=Task.objects.filter(user=request.user)
    
    search=request.GET.get('search','')
    if search:
        tasks=tasks.filter(title__icontains=search)

    filter_by=request.GET.get('filter','all')
    if filter_by=='completed':
        tasks=tasks.filter(completed=True)
    elif filter_by=='pending':
        tasks=tasks.filter(completed=False)
    
    return render(request,"tasks/index.html",{"tasks":tasks,"search":search,"filter_by":filter_by})

@login_required
def add_task(request):
    if request.method=="POST":
        Task.objects.create(
            user=request.user,
            title=request.POST["title"],
            category=request.POST["category"],
            deadline=request.POST["deadline"],
        )
    return redirect("/")

@login_required
def complete_task(request,task_id):
    task=Task.objects.get(id=task_id)
    task.completed=True
    task.save()
    return redirect ("/")

@login_required
def delete_task(request,task_id):
    task=Task.objects.get(id=task_id)
    task.delete()
    return redirect ("/")

def register(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=User.objects.create_user(username=username, password=password)
        login(request,user)
        return redirect ("/")
    return render(request,"tasks/register.html")

def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            error = "Wrong username or password!"  # ← add this
    return render(request, "tasks/login.html", {"error": error})

def logout_view(request):
    logout(request)
    return redirect("/login/")
    
 






