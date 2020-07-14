from django.db import models
from datetime import datetime

# Create your models here.


class Patients(models.Model):
    bed_no = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=100)
    zipcode =  models.IntegerField()
    phone_no = models.IntegerField()
    Gender = models.CharField(max_length=3)
    prev_dess = models.CharField(default = "None",max_length = 100)
    lab_id = (models.CharField(max_length = 11))
    state = models.CharField(max_length =25)
    admit_time = models.DateTimeField(default=datetime.now())
    status = models.CharField(default = "Active",max_length = 20)


class XRayData(models.Model):
    bed_no = models.IntegerField()
    status = models.CharField(max_length = 10)
    accuracy = models.IntegerField()
    img = models.ImageField(upload_to = "x_ray_data")
    date_time = models.DateTimeField(default=datetime.now())