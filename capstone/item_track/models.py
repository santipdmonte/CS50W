from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Agrega campos personalizados aquí
    pass

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    barcode = models.CharField(max_length=64, blank=True, null=True)
    image = models.ImageField(upload_to="item_track/images", blank=True, null=True)
    category = models.ManyToManyField("Category", blank=True, related_name="items")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
    
    
    def serialize(self):
        if self.expiration_date is not None:
            expiration_date = self.expiration_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            expiration_date = None

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            # "image": self.image,
            # "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "expiration_date": expiration_date,
            "active": self.active
        }


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
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
    description = models.CharField(max_length=256, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class TransactionRecord(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name="transactions", blank=True, null=True)
    treatments = models.ManyToManyField("Treatment", related_name="transactions", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(max_length=64, blank=True, null=True)
    payment_status = models.CharField(max_length=64, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_reference = models.CharField(max_length=64, blank=True, null=True)
    payment_comments = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.id}] {self.name} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def serialize(self):
        if self.payment_date is not None:
            payment_date = self.payment_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            payment_date = None

        movements = [movement.serialize() for movement in self.movements.all()]

        print(movements)

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "client": self.client,
            # "treatments": self.treatments,
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S'),
            "total": self.total,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "payment_date": payment_date,
            "payment_amount": self.payment_amount,
            "payment_reference": self.payment_reference,
            "payment_comments": self.payment_comments,
            "movements": movements,
            "active": self.active
        }



class Movemets(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="movements", blank=True, null=True)
    observation = models.CharField(max_length=256, blank=True, null=True)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name="movements", blank=True, null=True)
    treatment = models.ForeignKey("Treatment", on_delete=models.CASCADE, related_name="movements", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=64, blank=True, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    TransactionRecord = models.ForeignKey("TransactionRecord", on_delete=models.CASCADE, related_name="movements", blank=True, null=True)

    def __str__(self):
        return f"{self.item} - {self.type} - {self.quantity}"
    
    def serialize(self):
        return {
            "id": self.id,
            "item": self.item.serialize(),
            "observation": self.observation,
            "client": self.client,
            "treatment": self.treatment,
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S'),
            "type": self.type,
            "quantity": self.quantity,
            "price": self.price,
            "total": self.total,
            # "TransactionRecord": self.TransactionRecord
        }



# TODO PetClass