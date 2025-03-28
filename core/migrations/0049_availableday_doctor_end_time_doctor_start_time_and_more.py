# Generated by Django 5.1.6 on 2025-03-27 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_doctor_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')], max_length=10, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='available_days',
            field=models.ManyToManyField(blank=True, to='core.availableday'),
        ),
    ]
