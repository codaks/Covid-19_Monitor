from django.db import models


class LabsLogin(models.Model):
    email_id = models.CharField(max_length=200)
    lab_name = models.CharField(max_length = 50)
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    zipcode = models.IntegerField()