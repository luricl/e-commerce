from django.contrib import admin
from auctions.models import User, Categories, AuctionListings, Bids, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(AuctionListings)
admin.site.register(Bids)
admin.site.register(Comments)