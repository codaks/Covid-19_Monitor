# Generated by Django 3.0.3 on 2020-05-12 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LabsLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.CharField(max_length=200)),
                ('lab_name', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('zipcode', models.IntegerField()),
            ],
        ),
    ]
