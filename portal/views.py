from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Invoice, Payment, Tenantprofile, Apartment

# Create your views here.
@login_required
def tenant_dashboard(request):
    # each user has one tenant profile
    tenant_profile = Tenantprofile.objects.get(user=request.user)
    invoices = Invoice.objects.filter(tenant=tenant_profile)
    payments = Payment.objects.filter(tenant=tenant_profile)
    context = {
        "tenant_profile": tenant_profile,
        "invoices": invoices,
        "payments": payments,
    }
    return render(request, "portal/tenant_dashboard.html", context)

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    # show all tenants and summery
    tenants = Tenantprofile.objects.all()
    invoices = Invoice.objects.all()
    payments = Payment.objects.all()
    context = {
        "tenants": tenants,
        "invoices": invoices,
        "payments": payments,
    }
    return render(request, "portal/admin_dashboard.html", context)

def apartments_list(request):
    apartments = Apartment.objects.all()
    context = {'apartments': apartments}
    return render(request, 'portal/apartments_list.html', context)

def dashboard(request):
    return render(request, 'portal/dashboard.html')

def bedsitters_list(request):
    apartments = Apartment.objects.prefetch_related('bedsitters').all()
    # For each apartment, filter bedsitters that are available
    for apartment in apartments:
        apartment.available_bedsitters = apartment.bedsitters.filter(tenantprofile__isnull=True)

    context = {'apartments': apartments}
    return render(request, 'portal/bedsitters_list.html', context)