# Generated by Django 4.1.3 on 2023-02-17 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalyearproject', '0005_alter_appointmentbooking_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentbooking',
            name='key',
            field=models.IntegerField(default=875431894588),
        ),
    ]
