# Generated by Django 3.2.9 on 2021-12-05 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0004_alter_ingredient_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='name',
        ),
    ]
