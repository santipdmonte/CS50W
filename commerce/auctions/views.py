from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Auction_listing, Bid, Comment

import utils


def index(request):
    return render(request, "auctions/index.html",{
        "listing": Auction_listing.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def listing_page(request, id):
    item = Auction_listing.objects.get(id = id)
    comments = Comment.objects.filter(listing = item)
    print("Listing_page")

    if request.method == "POST":
        print("ENTRO")

        type_form = request.POST["type_form"]
        

        if type_form == "new_bid":
            new_amount_bid = request.POST["new_bid"]
            if int(new_amount_bid) <=  int(item.actual_bid):
                return 404
            
            new_bid = Bid(
                    amount = new_amount_bid,
                    bidder = request.user,
                    listing = item
                )
            new_bid.save()

            item.actual_bid = new_amount_bid
            item.winner = request.user

            item.save()

            return render(request, "auctions/listing_page.html",{
                "listing": item,
                "comments": comments
            })
        elif type_form == "new_comment":
            new_comment = request.POST["new_comment"]
            comment = Comment(
                    comment = new_comment,
                    commenter = request.user,
                    listing = item
                )
            comment.save()

    if id:
        return render(request, "auctions/listing_page.html",{
            "listing": item,
            "comments": comments
        })
    return render(request, "auctions/inedx.html")

