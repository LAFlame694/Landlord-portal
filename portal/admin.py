from django.contrib import admin
from .models import Apartment, Bedsitter, TenantProfile, Invoice, Payment, Receipt

# Register your models here.
admin.site.register(Apartment)
admin.site.register(Bedsitter)
admin.site.register(TenantProfile)
admin.site.register(Payment)
admin.site.register(Receipt)

class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ("apartment",) #make apartment read only in admin

    def save_model(self, request, obj, form, change):
        # automaticcaly assign apartment based on the tenant's bedsitter
        if obj.tenant and obj.tenant.bedsitter:
            obj.apartment = obj.tenant.bedsitter.apartment
        super().save_model(request, obj, form, change)
admin.site.register(Invoice, InvoiceAdmin)