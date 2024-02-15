from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, AuctionListings, Categories, Bids, Comments

# fix categories bug: submit empty field
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
            
            try:
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

            except Categories.DoesNotExist:
                
                auction = AuctionListings(
                    title=request.POST.get("title"), 
                    author = author,
                    description=request.POST.get("description"),                     
                    starting_bid=float(request.POST.get("starting bid")), 
                    image_url=request.POST.get("image"),
                    category=None
                )
                
                auction.save()
                        
            return HttpResponseRedirect(reverse("index"))
        
        except Exception as e:
            messages.error(request, "Error")

    categories = Categories.objects.all()

    return render(request, "auctions/create_auction.html",{
                    "categories" : categories
                })
    

def show_auction(request, item):

    auction = AuctionListings.objects.get(title=item)
    bids = Bids.objects.filter(auction=auction)
    current_price = 0
    comments = Comments.objects.filter(auction=auction)
    
    print(comments)

    num_of_bids = 0
    winner = None
    in_watchlist = False

    if bids:
        current_price = bids.order_by('-value')[0].value
        min_bid = float(current_price) + 0.01
        winner = bids.order_by('-value')[0].user
        num_of_bids = len(bids)

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        
        if user.watchlist.filter(id=auction.id):
            in_watchlist = True

    return render(request, "auctions/auction.html", {
        "auction": auction,
        "bids": bids,
        "winner": winner,
        "current_price": current_price,
        "min_bid": min_bid,
        "num_of_bids": num_of_bids,
        "comments": comments,
        "in_watchlist": in_watchlist 
    })


def watchlist(request):

    auctions = request.user.watchlist.all()
    categories = Categories.objects.all()

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)

        if request.method == "POST":
            category = Categories.objects.get(name=request.POST.get("category"))
            auctions = auctions.filter(category=category)

    return render(request, "auctions/watchlist.html", {
            "auctions" : auctions,
            "categories" : categories
        })


def add_watchlist(request, auction_id):
    auction = AuctionListings.objects.get(id=auction_id)

    auction.users_watching.add(request.user)
    auction.save()

    messages.success(request, "Auction added to watchlist!")

    return HttpResponseRedirect(reverse(show_auction, kwargs={"item": auction.title}))


def remove_watchlist(request, auction_id):
    auction = AuctionListings.objects.get(id=auction_id)

    auction.users_watching.remove(request.user)
    auction.save()

    messages.warning(request, "Auction removed from watchlist!")

    return HttpResponseRedirect(reverse(show_auction, kwargs={"item": auction.title}))


def close_auction(request, auction_id):
    auction = AuctionListings.objects.get(id=auction_id)

    auction.active = False
    auction.save()

    return HttpResponseRedirect(reverse(show_auction, kwargs={"item": auction.title}))


def bid(request, auction_id):
    auction = AuctionListings.objects.get(id=auction_id)
    bid_value = request.POST["bid"]

    new_bid = Bids(user=request.user, auction=auction, value=bid_value)
    new_bid.save()

    messages.success(request, "Bid added!")

    return HttpResponseRedirect(reverse(show_auction, kwargs={"item": auction.title}))


def comment(request, auction_id):
    auction = AuctionListings.objects.get(id=auction_id)

    comment = Comments(user=request.user, auction=auction, body=request.POST["add_comment"])
    comment.save()

    messages.success(request, "Comment added!")

    return HttpResponseRedirect(reverse(show_auction, kwargs={"item": auction.title}))
