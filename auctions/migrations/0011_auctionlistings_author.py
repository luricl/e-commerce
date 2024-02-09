# Generated by Django 5.0.1 on 2024-02-08 11:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_comments_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='author',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='auction_author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
