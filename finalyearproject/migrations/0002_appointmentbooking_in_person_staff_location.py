# Generated by Django 4.1.3 on 2023-02-11 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalyearproject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentbooking',
            name='in_person',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
