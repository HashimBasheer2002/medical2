# Generated by Django 5.1.6 on 2025-03-17 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_researchdocument_researchprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambulancebooking',
            name='pickup_latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='ambulancebooking',
            name='pickup_longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
