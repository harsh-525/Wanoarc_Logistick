# Generated by Django 4.1.6 on 2023-03-13 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistick', '0017_orderdetail_status_alter_bag_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='fquestion',
            name='address',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('Placed', 'Placed'), ('Accepted', 'Accepted'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Rejected', 'Rejected')], default='placed', max_length=10),
        ),
    ]
