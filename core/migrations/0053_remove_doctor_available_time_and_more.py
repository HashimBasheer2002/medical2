# Generated by Django 5.1.6 on 2025-03-27 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_alter_doctor_available_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='available_time',
        ),
        migrations.AddField(
            model_name='doctor',
            name='available_end_time',
            field=models.TimeField(default='17:00'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='available_start_time',
            field=models.TimeField(default='09:00'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='available_days',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], default='Monday', max_length=255),
        ),
    ]
