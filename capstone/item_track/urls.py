from django.urls import path
from . import views

urlpatterns = [
    # Define tus URLs aquí
	path("", views.index, name="index"),
	path("vet", views.index, name="vet"),
    path("transaction", views.transaction, name="transaction"),
    path("transaction/<int:transaction_id>", views.transaction, name="transaction_id"),
]