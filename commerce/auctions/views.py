from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Auction_listing, Bid, Comment

import utils


def index(request):
    categories = Category.objects.all()
    active_listing = Auction_listing.objects.filter(active = True)

    return render(request, "auctions/index.html",{
        "categories": categories,
        "listing": active_listing
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
    
    whatchlist = active_user.whatchlist.all()
    is_in_watchlist = False
    if item in whatchlist:
        is_in_watchlist = True

    if request.method == "POST":

        type_form = request.POST["type_form"]

        if type_form == "close_bid":
            try:
                item.active = False
                item.save()
            except Exception as e:
                print(e)
        
        elif type_form == "add_watchlist":
            try:
                item_to_add = Auction_listing.objects.get(id=item.id)
                active_user.whatchlist.add(item_to_add)
                is_in_watchlist = True
            except Exception as e:
                print(e)

        elif type_form == "remove_watchlist":
            try:
                item_to_remove = Auction_listing.objects.get(id=item.id)
                print(f"{item_to_remove=}")
                print(f"{active_user=}")
                active_user.whatchlist.remove(item_to_remove)
                is_in_watchlist = False
            except Exception as e:
                print(e)

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

        elif type_form == "new_comment":
            new_comment = request.POST["new_comment"]
            comment = Comment(
                    comment = new_comment,
                    commenter = active_user,
                    listing = item
                )
            comment.save()

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
        return 404
    
    active_listing = Auction_listing.objects.filter(active = True, category = category)
    print(active_listing)
    return render(request, "auctions/index.html",{
            "categories": categories,
            "selected_category": category, 
            "listing": active_listing
        })



