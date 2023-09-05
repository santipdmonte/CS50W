from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
import json

from .models import User, Post


def index(request):
    user = request.user
    if not user.is_authenticated:
        user = None

    # Get all posts and order by most recent first
    posts = Post.objects.all().order_by('-created_at')
        
    # Add Pagination to the posts
    page_posts = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = page_posts.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_obj,
        "user": user
    })

def following(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "network/register.html")
    
    following = user.following.all()

    # User__in to check if the user is in the list of following
    # Order the post by most recent first
    posts = Post.objects.filter(user__in = following).order_by('-created_at')

    # Add Pagination to the posts
    page_posts = Paginator(posts, 4)
    page_number = request.GET.get('page')
    posts_obj = page_posts.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": posts_obj
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
    
@csrf_exempt
def profile(request, username):
    user = request.user
    if not user.is_authenticated:
        user = None

    if request.method == "PUT":
        # Get the user to follow
        user_to_follow = User.objects.get(username=username)

        # Check if the user is already following
        if user_to_follow in user.following.all():
            user.following.remove(user_to_follow)
            user_to_follow.followers.remove(user)
        else:
            user.following.add(user_to_follow)
            user_to_follow.followers.add(user)
        return JsonResponse(user_to_follow.serialize(), safe=False)

    # Gets the post from the profile and order by most recent
    profile = User.objects.get(username=username)
    posts = Post.objects.filter(user=profile).order_by('-created_at')

    # Add Pagination to the posts
    page_posts = Paginator(posts, 4)
    page_number = request.GET.get('page')
    posts_obj = page_posts.get_page(page_number)

    is_following = profile in user.following.all()

    return render(request, "network/profile.html", {
        "profile": profile,
        "posts": posts_obj,
        "user": user,
        "is_following": is_following
    })

@csrf_exempt
def postData(request, postId):
    if request.method == "PUT":
        # Get the user to follow
        post = Post.objects.get(id=postId)
        user = request.user

        # Check if the user is already following
        if user in post.liked_by.all():
            print("Unlike")
            post.liked_by.remove(user)
        else:
            print("Like")
            post.liked_by.add(user)

        return JsonResponse(post.serialize(), safe=False)
    return HttpResponse(status=400)

@csrf_exempt
def postEdit(request, postId):
    if request.method == "PUT":
        # Get the user to follow
        data = json.loads(request.body)
        post = Post.objects.get(id=postId)
        user = request.user

        # Check if the user is already following
        if user == post.user:
            post.title = data["title"]
            post.content = data["content"]
            post.edited = True
            post.save()
        else:
            print("Error: User not allowed to edit this post")

        return JsonResponse(post.serialize(), safe=False)
    return HttpResponse(status=400)
    