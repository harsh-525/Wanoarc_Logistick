# Generated by Django 4.1.6 on 2023-02-20 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistick', '0015_bag'),
    ]

    operations = [
        migrations.AddField(
            model_name='bag',
            name='total_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
