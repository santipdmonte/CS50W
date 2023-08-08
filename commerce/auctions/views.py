from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

from django.core.exceptions import ValidationError

from .models import User, Category, Auction_listing, Bid, Comment

import utils

# To validate a decorator
def is_user_authenticated(user):
    return user.is_authenticated

def index(request):
    categories = Category.objects.all()
    active_listing = Auction_listing.objects.filter(active = True)
    
    user_watchlist = []
    if request.user.is_authenticated:
        user_watchlist = request.user.watchlist.filter(active = True)

    return render(request, "auctions/index.html",{
        "categories": categories,
        "listing": active_listing,
        "watchlist": user_watchlist,
        "message": "Active Listing"
    })


def login_view(request):
    categories = Category.objects.all()

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
            return render(request, "auctions/login.html", {
                "categories": categories,
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    categories = Category.objects.all()

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "categories": categories,
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "categories": categories,
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def listing_page(request, id):
    item = Auction_listing.objects.get(id = id)
    categories = Category.objects.all()
    comments = Comment.objects.filter(listing = item)
    active_user = request.user
    
    user_watchlist = []
    if request.user.is_authenticated:
        user_watchlist = active_user.watchlist.all()

    is_in_watchlist = False
    if item in user_watchlist:
        is_in_watchlist = True

    if request.method == "POST":

        type_form = request.POST["type_form"]

        
        # Add/remove item from watchlist 
        if type_form == "add_watchlist":
            try:
                item_to_add = Auction_listing.objects.get(id=item.id)
                active_user.watchlist.add(item_to_add)
                is_in_watchlist = True
            except Exception as e:
                print(e)
        elif type_form == "remove_watchlist":
            try:
                item_to_remove = Auction_listing.objects.get(id=item.id)
                print(f"{item_to_remove=}")
                print(f"{active_user=}")
                active_user.watchlist.remove(item_to_remove)
                is_in_watchlist = False
            except Exception as e:
                print(e)

        # Close the actual bid
        elif type_form == "close_bid":
            try:
                item.active = False
                item.save()
            except Exception as e:
                print(e)

        # Create a new bid
        elif type_form == "new_bid":
            new_amount_bid = request.POST["new_bid"]
            if int(new_amount_bid) <=  int(item.actual_bid):
                return 404
            
            new_bid = Bid(
                    amount = new_amount_bid,
                    bidder = active_user,
                    listing = item
                )
            new_bid.save()

            item.actual_bid = new_amount_bid
            item.winner = active_user
            item.save()

        # Add a comment
        elif type_form == "new_comment":
            new_comment = request.POST["new_comment"]
            comment = Comment(
                    comment = new_comment,
                    commenter = active_user,
                    listing = item
                )
            comment.save()

        message = request.POST["from"]
        if  message == "from_index":
            return index(request)
        elif message == "from_watchlist":
            return watchlist(request)
    
    if id:
        return render(request, "auctions/listing_page.html",{
            "categories": categories,
            "listing": item,
            "comments": comments,
            "is_in_watchlist": is_in_watchlist
        })
    return render(request, "auctions/inedx.html")


def category_page(request, category_id):
    category = Category.objects.get(id=category_id)
    categories = Category.objects.all()

    # Validate that the category exists
    if category not in categories:
        raise Exception("An internal server error occurred.")
    
    active_listing = Auction_listing.objects.filter(active = True, category = category)
    return render(request, "auctions/index.html",{
            "categories": categories,
            "selected_category": category, 
            "listing": active_listing,
            "message": "Active Listing"
        })

@user_passes_test(is_user_authenticated, login_url='/login') # If the user ir not login go to login.html
def watchlist(request):
    categories = Category.objects.all()

    user_watchlist = request.user.watchlist.filter(active = True)

    return render(request, "auctions/index.html",{
            "categories": categories,
            "listing": user_watchlist,
            "watchlist": user_watchlist,
            "message": "Watchlist"
        })


@user_passes_test(is_user_authenticated, login_url='/login') # If the user ir not login go to login.html
def new_auction(request):
    categories = Category.objects.all()

    if request.method == "POST":

        image_url = request.POST["image_url"]
        if image_url == "":
            image_url = '/static/auctions/images/not_image.jpg'
    
        category = Category.objects.get(id = request.POST["category"])

        new_auction = Auction_listing(
            title = request.POST["title"],
            description = request.POST["description"],
            image_url = image_url,
            starting_bid = request.POST["starting_bid"],
            actual_bid = request.POST["starting_bid"],
            category = category,
            active = True,
            owner = request.user
        )
        new_auction.save()
    
        active_listing = Auction_listing.objects.filter(active = True)
        return render(request, "auctions/index.html",{
            "categories": categories,
            "listing": active_listing
        })

    return render(request, "auctions/new_auction.html",{
            "categories": categories
        })

@user_passes_test(is_user_authenticated, login_url='/login') # If the user ir not login go to login.html
def my_active_listing(request):
    categories = Category.objects.all()
    active_listing = Auction_listing.objects.filter(active = True, owner = request.user)
    return render(request, "auctions/index.html",{
        "categories": categories,
        "listing": active_listing,
        "message": "My Actives listings"
    })
    
