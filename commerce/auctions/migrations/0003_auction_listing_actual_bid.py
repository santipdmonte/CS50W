# Generated by Django 4.2.3 on 2023-08-02 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listing_category_comment_bid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='actual_bid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
