# Generated by Django 4.1.6 on 2023-02-12 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistick', '0013_stock_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='details',
            field=models.TextField(default='', max_length=1000),
        ),
    ]
