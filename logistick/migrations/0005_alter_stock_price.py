# Generated by Django 4.1.6 on 2023-02-08 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistick', '0004_rename_is_vendor_fquestion_is_vendor_stock_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]