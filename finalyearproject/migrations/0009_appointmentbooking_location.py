# Generated by Django 4.1.3 on 2023-02-18 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalyearproject', '0008_alter_appointmentbooking_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentbooking',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]