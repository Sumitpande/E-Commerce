from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="createListing"),
    path("listing", views.listing, name="listing"),
    path("catlog", views.categories, name="categories"),
    path("catlog/<str:cat>", views.categories_view, name="categories_view"),
    path("<int:id>", views.displayItem, name="displayItem"),
    path("watchlist",views.watchlist, name="watchlist"),
    path("watchlistA/<int:id>",views.addToWatchlist, name="addToWatchlist"),
    path("watchlistR/<int:id>",views.removeFromWl, name="removeFromWl"),
    path("endBid/<int:id>", views.endBid, name="endBid")
   
]
