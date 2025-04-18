# Generated by Django 5.1.6 on 2025-03-04 06:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_remove_doctor_hospital_doctor_affiliated_hospitals'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_doctors', to='core.hospital'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='affiliated_hospitals',
            field=models.ManyToManyField(related_name='affiliated_doctors', to='core.hospital'),
        ),
    ]
