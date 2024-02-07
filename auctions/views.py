from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, AuctionListings, Bids, Comments


def index(request):
    all_listings = AuctionListings.objects.filter(active=True)

    return render(request, "auctions/index.html", {"listings":all_listings})

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

            auction = AuctionListings(
                title=request.POST.get("title"), 
                description=request.POST.get("description"),                     
                starting_bid=float(request.POST.get("starting bid")), 
                image_url=request.POST.get("image")
            )
            
            auction.save()
            
            messages.success(request, "Listing created!")
            
            return HttpResponseRedirect(reverse("index"))
        except:
            messages.error(request, "action failed!")

    return render(request, "auctions/create_listing.html")
    
def show_listing(request, item):

    listing = AuctionListings.objects.get(title=item)

    
    return render(request, "auctions/listing.html", {
        "listing": listing 
    })