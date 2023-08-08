from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction_listing", blank=True, related_name="watchlist")

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name.capitalize()}"

class Auction_listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.IntegerField()
    actual_bid = models.IntegerField()
    image_url = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", null = True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True)

    def __str__(self):
        return f"{self.title.capitalize()}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="listing_bid")

    def __str__(self):
        return f"{self.bidder}: {self.listing} ${self.amount}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=256)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="listing_comment") 

    def __str__(self): 
        return f"{self.commenter}: {self.comment}"
    









