from django.urls import path
from . import views

urlpatterns = [
    # Define tus URLs aquí
	path("", views.index, name="index"),
]