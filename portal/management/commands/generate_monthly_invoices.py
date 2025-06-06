from django.core.management.base import BaseCommand
from django.utils import timezone
from portal.models import Tenantprofile, Invoice
from datetime import date

class Command(BaseCommand):
    help = 'Generate monthly rent invoices for all tenants'

    def handle(self, *args, **options):
        today = date.today()
        for tenant in Tenantprofile.objects.all():
            # Avoid duplicate invoice for same month
            if not Invoice.objects.filter(tenant=tenant, description__icontains=today.strftime('%B %Y')).exists():
                Invoice.objects.create(
                    tenant=tenant,
                    description=f'Rent for {today.strftime("%B %Y")}',
                    amount=10000,  # You can pull this from a settings or tenant field
                    due_date=date(today.year, today.month, 5),  # e.g., due by 5th of the month
                )
        self.stdout.write(self.style.SUCCESS('Monthly invoices generated.'))