from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like


def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html", {
        "posts": posts
    })

def following(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "network/register.html")
    
    following = user.following.all()
    
    # User__in to check if the user is in the list of following
    posts = Post.objects.filter(user__in = following)
    return render(request, "network/index.html", {
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def new_post(request):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        content = request.POST["content"]

        print(f"{user} | {title} | {content}")

        # Attempt to upload the post
        try:
            post = Post(
                user = user, 
                title = title, 
                content = content
            )
            post.save()
        except Exception as e:
            print(request, "network/new_post.html", {
                "message": f"Error: {e}"
            })
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "network/new_post.html")
    
def profile(request, username):
    user = request.user
    if not user.is_authenticated:
        user = None

    profile = User.objects.get(username=username)
    posts = Post.objects.filter(user=profile)
    return render(request, "network/profile.html", {
        "profile": profile,
        "posts": posts,
        "user": user
    })
    
