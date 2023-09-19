from django.urls import path
from . import views

urlpatterns = [
    # Define tus URLs aquí
	path("", views.index, name="index"),
	path("vet", views.vet, name="vet"),
	path("front_desk", views.front_desk, name="front_desk"),
    path("transaction", views.transaction, name="transaction"),
    path("manage", views.manage, name="manage"),
    path("status", views.status, name="status"),
    path("item/barcode/<str:barcode>", views.item_by_barcode, name="barcode"),
    path("item/update/<str:item_id>", views.update_item_by_id, name="update_item_by_id"),
    path("transaction/<int:transaction_id>", views.transaction, name="transaction_id"),
    path("movement/<int:movement_id>", views.movement, name="movement"),
]