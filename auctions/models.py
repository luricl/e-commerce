from django.contrib.auth.models import AbstractUser
from django.db import models

# Challenge: reimplement this
class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class AuctionListings(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=150)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    category = models.CharField(max_length=64)
    users_watching = models.ManyToManyField(User)

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
    body = models.CharField(max_length=10000)
    time = models.DateTimeField()
