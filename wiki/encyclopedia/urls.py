from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),  # (Take the value of the str and save it as title, call enrty fucntion, alias url: entry)
    path("/new_page", views.new_page, name="new_page")
]

