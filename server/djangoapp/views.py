from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import requests
from .models import  CarDealer
from .restapis import get_dealer_reviews_from_cf
from .restapis import post_request
from django.urls import reverse


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def  get_dealer_details(request, dealer_id):
    # Call get_dealer_reviews_from_cf method in restapis.py
    reviews = get_dealer_reviews_from_cf(dealer_id)

    # Append the list of reviews to the context
    context = {
        'reviews': reviews,
    }

    # Return a HttpResponse
    return render(request, 'dealer_details.html', context)


# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships



def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/cf0035e1-499c-464f-9ca1-9e3d938b50ce/dealership-package/get-dealership"
        # Call get_dealers_from_cf function to get dealerships
        dealerships = get_dealers_from_cf(url)
        # Create a list of dealer_names as rows for the table
        dealer_names = [dealer.short_name for dealer in dealerships]
        # Update the context dictionary with the dealer_names
        context = {'dealer_names': dealer_names}
        # Render the 'djangoapp/index.html' template with the updated context dictionary
        return render(request, 'djangoapp/index.html', context)




# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def about_view(request):
    # Add logic for rendering about us page here
    return render(request, 'about.html')

def contact_view(request):
    # Add logic for rendering contact us page here
    return render(request, 'contact.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')  # Redirect to index view or any other view
        else:
            messages.error(request, 'Invalid username or password.')  # Display error message
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('djangoapp:index')  # Redirect to index view or any other view
    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signout_view(request):
    logout(request)
    return redirect('djangoapp:index')  # Redirect to index view or any other view

def get_dealers_from_cf(url):
    # Make REST call to review-get cloud function service
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        # Load JSON results into a list
        json_results = response.json()

        # Create a list to store CarDealer objects
        dealers = []

        # Loop through the JSON results and create CarDealer objects
        for result in json_results:
            dealer = CarDealer(
                address=result['address'],
                city=result['city'],
                full_name=result['full_name'],
                id=result['id'],
                lat=result['lat'],
                long=result['long'],
                short_name=result['short_name'],
                st=result['st'],
                zip=result['zip']
            )
            dealers.append(dealer)

        return dealers
    else:
        # Handle the response if it's not successful
        # e.g. return an empty list or raise an exception
        return []

def add_review(request, dealer_id):
    if request.method == "POST":
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = request.user.username
        review["dealership"] = dealer_id
        review["review"] = request.POST.get("review", "")
        review["purchase"] = request.POST.get("purchase", False)
        json_payload = {"review": review}
        url = 'https://us-south.functions.appdomain.cloud/api/v1/web/cf0035e1-499c-464f-9ca1-9e3d938b50ce/dealership-package/post_review'
        post_request(url, json_payload, dealerId=dealer_id)
    return render(request, "add_review.html", {"dealer_id": dealer_id})

