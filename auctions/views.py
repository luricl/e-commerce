from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, AuctionListings, Categories, Bids, Comments


def index(request):
    auctions = AuctionListings.objects.filter(active=True)
    categories = Categories.objects.all()

    if request.method == "POST":
        category = Categories.objects.get(name=request.POST.get("category"))
        auctions = auctions.filter(category=category)

    return render(request, "auctions/index.html", {
            "auctions" : auctions,
            "categories" : categories
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


def create_listing(request):
    if request.method == "POST":
        try:
            author = request.user
            category = Categories.objects.get(name=request.POST.get("category"))

            auction = AuctionListings(
                title=request.POST.get("title"), 
                author = author,
                description=request.POST.get("description"),                     
                starting_bid=float(request.POST.get("starting bid")), 
                image_url=request.POST.get("image"),
                category=category
            )
            
            auction.save()
                        
            return HttpResponseRedirect(reverse("index"))
        except:
            messages.error(request, "action failed!")

    categories = Categories.objects.all()

    return render(request, "auctions/create_auction.html",{
                    "categories" : categories
                })
    

def show_auction(request, item):

    auction = AuctionListings.objects.get(title=item)
    bids = Bids.objects.filter(auction_id=auction)

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        watchlist = user.watchlist.all()

        print(watchlist)

        if request.method == "POST":
            # addition or removal from watchlist
            watchlist = User.object.filter(username=request.username)
            
            

            # post bids(if user is authenticaded)
            # close auction if user is the author of the listing
            # post comments if user is authenticated

        return render(request, "auctions/auction.html", {
            "auction": auction,
            "number_of_bids": len(bids),
            "watchlis": watchlist 
        })
    else:
        return render(request, "auctions/auction.html", {
            "auction": auction,
            "number_of_bids": len(bids),
        })


def add_watchlist(request):
    pass

def remove_watchlist(request):
    pass

def watchlist(request):
    user = User.objects.get(username=request.user.username)
    
    auctions = user.watchlist.all()
    categories = Categories.objects.all()

    if request.method == "POST":
        category = Categories.objects.get(name=request.POST.get("category"))
        auctions = auctions.filter(category=category)

    return render(request, "auctions/watchlist.html", {
            "auctions" : auctions,
            "categories" : categories
        })
