from django.urls import path
from . import views

urlpatterns = [
    # Define tus URLs aquí
	path("", views.index, name="index"),
	path("vet", views.vet, name="vet"),
	path("front_desk", views.front_desk, name="front_desk"),
    path("transaction", views.transaction, name="transaction"),
    path("transaction/<int:transaction_id>", views.transaction, name="transaction_id"),
]