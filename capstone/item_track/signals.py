from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from django.db.models import Sum
from .models import Movements

@receiver(post_save, sender=Movements)
@receiver(post_delete, sender=Movements)
def update_transaction_total(sender, instance, **kwargs):
    transaction = instance.TransactionRecord
    if transaction:
        # Recalcula el total sumando los movimientos asociados
        total = transaction.movements.aggregate(Sum('total'))['total__sum'] or 0
        transaction.total = total
        transaction.save()

@receiver(post_delete, sender=Movements)
def update_item_stock(sender, instance, **kwargs):
    # Verify if the movement is a sell and has an item
    if instance.type == 'Sell' and instance.item:
        item = instance.item
        # Update the item stock
        item.stock += instance.quantity
        item.save()