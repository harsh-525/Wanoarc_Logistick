# Generated by Django 4.1.6 on 2023-03-13 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistick', '0021_fquestion_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fquestion',
            name='address',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
