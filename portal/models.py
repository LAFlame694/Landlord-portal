from django.db import models
from django.contrib.auth.models import User

class Apartment(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.address})"

class Bedsitter(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='bedsitters', on_delete=models.CASCADE)
    number = models.CharField(max_length=255, unique=True)
    # Remove is_available

    def __str__(self):
        return f"{self.apartment.name} - Room {self.number}"

class Tenantprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bedsitter = models.OneToOneField(Bedsitter, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Invoice(models.Model):
    tenant = models.ForeignKey(Tenantprofile, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.id} for {self.tenant}"

class Payment(models.Model):
    tenant = models.ForeignKey(Tenantprofile, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant} on {self.date.strftime('%Y-%m-%d')}"

class Receipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=50, unique=True)
    date_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.receipt_number} for {self.payment}"