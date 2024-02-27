# Generated by Django 5.0.2 on 2024-02-25 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_rename_starting_bid_auctionlistings_starting_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='current_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winning_auctions', to='auctions.bids'),
        ),
    ]
