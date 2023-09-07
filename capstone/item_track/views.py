from django.shortcuts import render

from .models import User, Item, Client, Category, Treatment, TransactionRecord, Movemets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request):
    items = Item.objects.all()
    treatments = Treatment.objects.all()

    return render(request, "item_track/index.html",{
        'items': items,
        'treatments': treatments
    })

def vet(request):
    items = Item.objects.all()
    treatments = Treatment.objects.all()

    return render(request, "item_track/vet.html",{
        'items': items,
        'treatments': treatments
    })

def front_desk(request):

    if request.method == "PUT":
        data = json.loads(request.body)
        transaction_id = data['consult_id']

        transaction = TransactionRecord.objects.get(id=transaction_id)
        transaction.active = False
        transaction.save()

    consults = TransactionRecord.objects.filter(active=True)

    # TODO add history
    past_consults = TransactionRecord.objects.filter(active=False).order_by('-date')

    return render(request, "item_track/front_desk.html",{
        'consults': consults,
        'past_consults': past_consults
    })

def transaction(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)

            # Create transaction
            transaction = TransactionRecord(
                name = data[0]['name'],
                description = data[0]['observation'],
            )
            transaction.save()

            transaction_total = 0

            # Create Movements
                # data[0] clients data
            for movement in data[1:]:
                movement = Movemets(
                    item = Item.objects.get(id=movement['item_id']),
                    quantity = movement['amount'],
                    price = movement['price'],
                    total = float(movement['amount']) * float(movement['price']),
                    type = "Sell",
                    TransactionRecord = transaction
                )
                movement.save()
                transaction_total += movement.total

            transaction.total = transaction_total
            transaction.save()

            return JsonResponse({'message': 'Datos procesados correctamente'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error en el formato JSON'}, status=400)

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





