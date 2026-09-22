
from django.contrib import admin
from .models import BloodStock, BloodRequest, DonationRequest

admin.site.register(BloodStock)
admin.site.register(BloodRequest)
admin.site.register(DonationRequest)