# Generated by Django 4.1.3 on 2023-03-30 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalyearproject', '0014_appointmentbooking_user_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentbooking',
            name='cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='appointmentbooking',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]