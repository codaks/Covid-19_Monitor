# Generated by Django 3.0.3 on 2020-05-13 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_patients_lab_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='admit_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 13, 18, 19, 16, 52078)),
        ),
    ]
