from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from auction.models import User, Brand, Category, Bid, Listing, Comment
from .forms import RegistrationForm, CreateListingForm, LoginForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

def index(request):
    site_name = "Motorcycles Auction Club"

    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    allBrands = Brand.objects.all()

    return render(request, "auction/index.html", {
        "site_name": site_name,
        "listings": activeListings,
        "categories": allCategories,
        "brands": allBrands
    })

def displayBrand(request):
    if request.method == "POST":
        # Retrieve the 'brand' parameter from the POST data
        brandFromForm = request.POST.get('brand')

        # Use get_object_or_404 for better error handling
        brand = get_object_or_404(Brand, brandName=brandFromForm)

        # Use select_related to fetch related objects efficiently
        activeListings = Listing.objects.filter(isActive=True, brand=brand).select_related('brand')

        # Retrieve all Brand objects from the database
        allBrands = Brand.objects.all()

        # Render the 'auction/index.html' template with the data
        return render(request, "auction/index.html", {
            "listings": activeListings,
            "brands": allBrands
        })


# def displayCategory(request):
#     if request.method == "POST":
#         categoryFromForm = request.POST['category']
#         category = Category.objects.get(categoryName=categoryFromForm)
#         activeListings = Listing.objects.filter(isActive=True, category=category)
#         allCategories = Category.objects.all()
#         return render(request, "auction/index.html", {
#             "listings": activeListings,
#             "categories": allCategories
#         })
    
        

def displayCategory(request):
    site_name = "Motorcycles Auction Club"
    if request.method == "POST":
        brandName = request.POST.get('brand')
        categoryName = request.POST.get('category')

        # Use select_related to fetch related data in a single query
        activeListings = Listing.objects.filter(isActive=True).select_related('category', 'brand')

        # Optionally filter by brand
        if brandName:
            brand = get_object_or_404(Brand, brandName=brandName)
            activeListings = activeListings.filter(brand=brand)

        # Optionally filter by category
        if categoryName:
            category = get_object_or_404(Category, categoryName=categoryName)
            activeListings = activeListings.filter(category=category)

        # Optionally pass the selected brand and category to the template
        selectedBrand = brand if brandName else None
        selectedCategory = category if categoryName else None

        if not activeListings.exists():
            return render(request, "auction/error.html", {"message": "No matching listings found."})
        else:
            allBrands = Brand.objects.all()
            allCategories = Category.objects.all()
            return render(request, "auction/index.html", {
                "site_name":site_name,
                "listings": activeListings,
                "brands": allBrands,
                "categories": allCategories,
                "selectedBrand": selectedBrand,
                "selectedCategory": selectedCategory,
            })

    else:
        return render(request, "auction/error.html", {"message": "Invalid request"})



@login_required
def createListing(request):
    if request.method == "GET":
        site_name = "Motorcycles Auction Club"
        form = CreateListingForm()
        return render(request, "auction/create.html", {"form": form, "site_name":site_name})
    else:
        form = CreateListingForm(request.POST)
        if form.is_valid():
            with transaction.atomic():      
                name = form.cleaned_data['name']
                imageurl = form.cleaned_data['imageurl']
                brand = form.cleaned_data['brand']
                category = form.cleaned_data['category']
                price = form.cleaned_data['price']
                description = form.cleaned_data['description']
                

                currentUser = request.user
                categoryData = Category.objects.get(categoryName=category)
                brandData = Brand.objects.get(brandName=brand)

                bid = Bid(bid=int(price), user=currentUser)
                bid.save()

                newListing = Listing(
                    name=name,
                    imageurl=imageurl,
                    brand=brandData,
                    category=categoryData,
                    price=bid,
                    description=description,
                    owner=currentUser
                )

                newListing.save()

                return HttpResponseRedirect(reverse('index'))
        else:
            # Form is not valid, handle the error or display an error message
            return render(request, "auction/create.html", {"form": form})


def listing(request, id):
    site_name = "Motorcycles Auction Club"
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auction/listing.html", {
        "listing":listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "site_name": site_name
    })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auction/listing.html", {
        "listing":listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Congratulations! Auction is Closed."
    })

def watchlist(request):
    site_name = "Motorcycles Auction Club"
    currentUser = request.user
    listings = currentUser.listingWatchList.all()
    return render(request, "auction/watchlist.html", {
        "site_name":site_name,
        "listings": listings
    })

def removeWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currnetUser = request.user
    listingData.watchlist.remove(currnetUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currnetUser = request.user
    listingData.watchlist.add(currnetUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

@login_required
def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']

    newComment = Comment(
        author = currentUser,
        listing = listingData,
        message = message
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

@login_required
@transaction.atomic
def addBid(request, id):
    try:
        newBid = int(request.POST['newBid'])
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Invalid bid value")

    listingData = get_object_or_404(Listing, pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username


    if  listingData.end_time >= (timezone.now() + timedelta(days=1)):
        # Auction has already ended
        message = "Auction has already ended."
        update = False
    elif newBid > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=newBid)
        updateBid.save()
        listingData.price = updateBid
        listingData.save()

        # Check if the auction should be marked as expired
        if listingData.end_time <= (timezone.now() + timedelta(days=1)):
            listingData.isExpired = True
            listingData.save()

        message = "Bid updated successfully"
        update = True
    else:
        message = "Bid update failed. Please enter a higher bid."
        update = False

    return render(request, "auction/listing.html", {
        "listing": listingData,
        "message": message,
        "update": update,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner
    })

def login_view(request):
    site_name = "Motorcycles Auction Club"
    if request.method == "POST":

        # Bind the form with the POST data
        form = LoginForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # If the form is valid, attempt to sign the user in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                form.add_error(None, "Invalid username and/or password.")

    else:
        # If the request method is not POST, create an instance of the form
        form = LoginForm()

    # Render the login page with the form
    return render(request, "auction/login.html", {
        "form": form,
        "site_name": site_name
})  


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    site_name = "Motorcycles Auction Club"

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('index'))
    else:
        form = RegistrationForm()

    return render(request, 'auction/register.html', {
        'form': form,
        "site_name": site_name
})


def user_profile(request):
    currentuser = request.user
    site_name = "Motorcycles Auction Club"

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=currentuser)
        if form.is_valid():
            form.save()
            return redirect('user')  # Redirect to the user profile page
    else:
        form = UserProfileForm(instance=currentuser)

    return render(request, 'auction/user.html', {
        'form': form,
        "site_name": site_name
})


def edit_profile(request):
    currentuser = request.user
    site_name = "Motorcycles Auction Club"

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=currentuser)
        if form.is_valid():
            form.save()
            return redirect('user')  # Redirect to the user profile page
    else:
        form = UserProfileForm(instance=currentuser)

    return render(request, 'auction/edit.html', {'form': form, "site_name": site_name})