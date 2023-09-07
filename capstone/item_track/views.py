from django.shortcuts import render

from .models import User, Item, Client, Category, Treatment, TransactionRecord

# Create your views here.
def index(request):
    items = Item.objects.all()
    treatments = Treatment.objects.all()

    return render(request, "item_track/index.html",{
        'items': items,
        'treatments': treatments
    })


def transaction(request, transaction_id):
    if request.method == "POST":
        pass

    if request.method == "PUT":
        pass






def create_item(request):
    if request.method == "POST":
        pass


def update_item(request):
    if request.method == "PUT":
        pass


# Create treatment
def create_trearment(request):
    if request.method == "POST":
        pass


def update_treatment(request):
    if request.method == "PUT":
        pass


def create_category(request):
    if request.method == "POST":
        pass

 
def update_category(request):
    if request.method == "PUT":
        pass





