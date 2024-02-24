from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

class AuctionListings(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="auctions")
    image_url = models.URLField()
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, blank=True, null=True, related_name="auctions")
    creation_date = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.ForeignKey('Bids', on_delete=models.PROTECT, related_name="winning_auctions")
    description = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    users_watching = models.ManyToManyField(User, blank=True, related_name="watchlist")

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="bids")
    value = models.DecimalField(max_digits=10, decimal_places=2)

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="comments")
    creation_date = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=10000)