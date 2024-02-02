from django.contrib.auth.models import AbstractUser
from django.db import models

# Challenge: reimplement this
class User(AbstractUser):
    # add reference to listings that belong to the user's watchlist
    pass

class AuctionListings(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    state = models.BooleanField(default=True)
    description = models.CharField(max_length=64)
    starting_bid = models.DecimalField(max_digits=1000000, decimal_places=2)
    image = models.URLField()
    category = models.CharField(max_length=64)

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_author")
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="target_auction")
    value = models.FloatField()

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    auction_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="commented_auction")
    body = models.CharField(max_length=10000)
    time = models.DateTimeField()
