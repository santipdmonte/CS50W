# Generated by Django 4.2.3 on 2023-08-05 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_user_whatchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='whatchlist',
            new_name='watchlist',
        ),
    ]
