from django.db import models
from django.contrib.auth.models import User

class Apartment(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.address})"
    
    class Meta:
        verbose_name_plural = "Apartments"

class Bedsitter(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='bedsitters', on_delete=models.CASCADE)
    number = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.apartment.name} - Room {self.number}"
    
    class Meta:
        verbose_name_plural = "Bedsitters"

class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bedsitter = models.OneToOneField(Bedsitter, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=255)
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
    class Meta:
        verbose_name = "Tenant Profile"
        verbose_name_plural = "Tenant Profiles"

class Invoice(models.Model):
    tenant = models.ForeignKey(TenantProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="invoices")

    def __str__(self):
        return f"Invoice #{self.id} for {self.tenant}"
    
    class Meta:
        verbose_name_plural = "Invoices"

class Payment(models.Model):
    tenant = models.ForeignKey(TenantProfile, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant} on {self.date.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name_plural = "Payments"

class Receipt(models.Model):
    tenant = models.ForeignKey(TenantProfile, on_delete=models.CASCADE, null=True, blank=True)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=50, unique=True)
    date_issued = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.payment and (not self.tenant):
            self.tenant = self.payment.tenant
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt #{self.receipt_number} for {self.payment}"
    
    class Meta:
        verbose_name_plural = "Receipts"