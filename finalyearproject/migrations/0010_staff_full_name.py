# Generated by Django 4.1.3 on 2023-02-18 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalyearproject', '0009_appointmentbooking_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='<django.db.models.query_utils.DeferredAttribute object at 0x000001FE36F7DA80><django.db.models.query_utils.DeferredAttribute object at 0x000001FE36F7DB10>'),
        ),
    ]
