from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_auction", views.new_auction, name="new_auction"),
    path("category/<str:category_id>", views.category_page, name="category_page"),
    path("<str:id>", views.listing_page, name="listing_page")
]
