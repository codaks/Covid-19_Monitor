from django.contrib import admin
from .models import Patients
from .models import XRayData

# Register your models here.
admin.site.register(Patients)
admin.site.register(XRayData)
