from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Agrega campos personalizados aquí
    pass

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    image = models.ImageField(upload_to="item_track/images", blank=True)
    category = models.ManyToManyField("Category", blank=True, related_name="items")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    stock = models.IntegerField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Treatment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class TransactionRecord(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name="transactions", blank=True)
    items = models.ManyToManyField("Item", blank=True, related_name="transactions")
    treatments = models.ManyToManyField("Treatment", blank=True, related_name="transactions")
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    payment_method = models.CharField(max_length=64, blank=True)
    payment_status = models.CharField(max_length=64, blank=True)
    payment_date = models.DateTimeField(blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    payment_reference = models.CharField(max_length=64, blank=True)
    payment_comments = models.CharField(max_length=256, blank=True)
    active = models.BooleanField(default=True)



class Movemets(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="movements", blank=True)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name="movements", blank=True)
    treatment = models.ForeignKey("Treatment", on_delete=models.CASCADE, related_name="movements", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=64, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)



# TODO PetClass