from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),  # (Take the value of the str and save it as title, call enrty fucntion, alias url: entry)
    path("/newpage", views.newpage, name="newpage")
]

