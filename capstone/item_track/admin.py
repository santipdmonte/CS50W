from django.contrib import admin
from .models import User, Item, Client, Category, Treatment, TransactionRecord, Movements

# Register your models here.
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Treatment)
admin.site.register(TransactionRecord)
admin.site.register(Movements)