# Generated by Django 5.0.1 on 2024-02-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auctionlistings_users_watching_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='description',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='title',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]