from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("user/", views.user_profile, name="user"),
    path('user/edit/', views.edit_profile, name='edit_profile'), 
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("displayBrand", views.displayBrand, name="displayBrand"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removeWatchList/<int:id>", views.removeWatchList, name="removeWatchList"),
    path("addWatchList/<int:id>", views.addWatchList, name="addWatchList"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction")
]
