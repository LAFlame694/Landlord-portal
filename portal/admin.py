from django.contrib import admin
from .models import Apartment, Bedsitter, Tenantprofile, Invoice, Payment, Receipt

# Register your models here.
admin.site.register(Apartment)
admin.site.register(Bedsitter)
admin.site.register(Tenantprofile)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Receipt)