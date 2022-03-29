from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.

# Home Page
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})

# About Page
def about(request):
    return render(request, 'blog/about.html')

# Contact Page
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard Page
def dashboard(request):
    # only show dashboard if user is logged in
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        # groups
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps})
    # but if user is not logged then send to login page
    else:
        return HttpResponseRedirect('/login/')

# logout Page
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# signup Page
def user_signup(request):
    # if request is post with requires fielded
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You have become an Author.')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    # if it is get request then send empty form
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})

# login Page
def user_login(request):    
    # if user is not logged in and user put username and pw in login form
    if not request.user.is_authenticated:
        # check if request is post 
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        # but if request is GET then send empty form
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    # but if user is already logged in then direct send to dashboard page no need to show logged in page
    else:
        return HttpResponseRedirect('/dashboard/')

# Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                # if form is valid then check all title,desc,etc
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()
                messages.success(request, 'New Post Added Successfully !!')
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

# update/Edit Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')                    
    else:
        return HttpResponseRedirect('/login/')
