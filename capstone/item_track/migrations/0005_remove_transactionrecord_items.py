# Generated by Django 4.2.3 on 2023-09-07 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item_track', '0004_movemets_transactionrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionrecord',
            name='items',
        ),
    ]
