from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listings/<str:item>/", views.show_auction, name="show_auction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:auction_id>/", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:auction_id>/", views.remove_watchlist, name="remove_watchlist"),
]