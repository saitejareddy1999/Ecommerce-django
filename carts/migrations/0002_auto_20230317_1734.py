# Generated by Django 3.1 on 2023-03-17 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='cartitem',
            new_name='cart',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='productc',
            new_name='product',
        ),
    ]
