from django.contrib.auth.models import AbstractUser
from django.db import models

# Challenge: reimplement this
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
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, blank=True, related_name="auctions")
    creation_date = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    users_watching = models.ManyToManyField(User, blank=True, related_name="watchlist")

    # https://www.geeksforgeeks.org/overriding-the-save-method-django-models/
    def save(self, *args, **kwargs):
        if not self.current_bid:
            self.current_bid = self.starting_bid
        super(AuctionListings, self).save(*args, **kwargs)

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_author")
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="target_auction")
    value = models.FloatField()

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="commented_auction")
    creation_date = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=10000)
    time = models.DateTimeField()
