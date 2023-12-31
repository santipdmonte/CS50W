from django.shortcuts import render

from .models import User, Item, Client, Category, Treatment, TransactionRecord, Movements
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal

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
    items = Item.objects.all()
    treatments = Treatment.objects.all()

    if request.method == "PUT":
        data = json.loads(request.body)
        transaction_id = data['consult_id']

        transaction = TransactionRecord.objects.get(id=transaction_id)
        transaction.active = False
        transaction.save()
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            transaction_id = data['consult_id']

            transaction = TransactionRecord.objects.get(id=transaction_id)

            # Update Stock
            item = Item.objects.get(id=data['item_id'])
            item.stock = item.stock - int(data['amount'])
            if item.stock < 0:
                return JsonResponse({'error': 'No hay suficiente stock'}, status=400)
            item.save()
            # TODO add restriction to stock
            
            # Create Movements and add to transaction
            movement = Movements(
                        item = item,
                        quantity = data['amount'],
                        price = data['price'],
                        total = Decimal(data['amount']) * Decimal(data['price']),
                        type = "Sell",
                        observation = data['observation'],
                        TransactionRecord = transaction
                    )
            movement.save()

            # return transaction.serialize()
            return JsonResponse({'message': 'Datos procesados correctamente', 'transaction': transaction.serialize()})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error en el formato JSON'}, status=400)

    consults = TransactionRecord.objects.filter(active=True).order_by
    # TODO add history
    past_consults = TransactionRecord.objects.filter(active=False).order_by('-date')

    return render(request, "item_track/front_desk.html",{
        'consults': consults,
        'past_consults': past_consults,
        'items': items,
        'treatments': treatments
    })


def transaction(request):
    if request.method == "POST":
        try:
            # data[0] clients data
            data = json.loads(request.body)

            # Create transaction
            transaction = TransactionRecord(
                name = data[0]['name'],
                description = data[0]['observation'],
            )
            transaction.save()

            transaction_total = 0

            # Create Movements
            for movement in data[1:]:
                treatment = Treatment.objects.get(id=movement['treatment_id'])

                movement = Movements(
                    treatment = treatment,
                    quantity = movement['amount'],
                    price = movement['price'],
                    total = Decimal(movement['amount']) * Decimal(movement['price']),
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


def manage(request):
        items = Item.objects.all()
        return render(request, "item_track/manage.html",{
        'items': items
        # 'treatments': treatments
    })


def item_by_barcode(request, barcode):
    try:
        item = Item.objects.get(barcode=barcode)
        return JsonResponse(item.serialize())
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


def update_item_by_id(request, item_id):
    if request.method == 'PUT':
        print("Update")
        try:
            data = json.loads(request.body)

            # Update item stock and price
            item = Item.objects.get(id=item_id)
            item.price = Decimal(data['itemPrice'])
            item.stock = item.stock + int(data['itemAmount'])
            item.save()

            # Create Movement
            if int(data['itemAmount']) > 0:
                movement = Movements(
                    item = item,
                    quantity = data['itemAmount'],
                    price = Decimal(data['itemPrice']),
                    type = "Buy"
                )
                movement.save()

            return JsonResponse({'message': 'Datos procesados correctamente'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error en el formato JSON'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def status(request):
    items = Item.objects.all()

    items = items.order_by('stock')

    # To send the data as JSON for print the inform
    # items_list = list(items.values()) 
    # items_json = json.dumps(items_list)

    return render(request, "item_track/status.html",{
        'items': items,
        # 'items_json': items_json
    })

def movement(request, movement_id):
    try:
        # Try to get the movement
        movement = Movements.objects.get(pk=movement_id)
        transaction = movement.TransactionRecord
    except Movements.DoesNotExist:
        # If the movement does not exist, return an error
        return JsonResponse({'error': 'El movimiento no existe.'}, status=404)

    if request.method == 'DELETE':
        # If the request is DELETE, delete the movement
        movement.delete()
        # Return a success message
        return JsonResponse({'message': 'El movimiento se eliminó correctamente.', 'transaction': transaction.serialize()}, status=200)

    # If the request is not DELETE, return an error
    return JsonResponse({'error': 'Método no permitido.'}, status=405)


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





