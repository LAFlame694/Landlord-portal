from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Invoice, Payment, Tenantprofile, Apartment, Bedsitter
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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

def bedsitters_list(request):
    apartments = Apartment.objects.prefetch_related('bedsitters').all()
    # For each apartment, filter bedsitters that are available
    for apartment in apartments:
        apartment.available_bedsitters = apartment.bedsitters.filter(tenantprofile__isnull=True)

    context = {'apartments': apartments}
    return render(request, 'portal/bedsitters_list.html', context)

def apartment_bedsitters(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    bedsitters = apartment.bedsitters.all().select_related('tenantprofile')
    context = {
        'apartment': apartment,
        'bedsitters': bedsitters,
    }
    return render(request, 'portal/apartment_bedsitters.html', context)

def tenant_apartment_select(request):
    apartments = Apartment.objects.all()
    return render(request, 'portal/tenant_apartment_select.html', {'apartments': apartments})

def tenantprofiles_by_apartment(request, apartment_id):
    apartment = get_object_or_404(Apartment, id=apartment_id)
    tenants = Tenantprofile.objects.filter(bedsitter__apartment=apartment).select_related('user', 'bedsitter')
    return render(request, 'portal/tenantprofiles_by_apartment.html', {'apartment': apartment, 'tenants': tenants})

@csrf_exempt
def mpesa_c2b_confirmation(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body.decode('utf-8'))
        print("Confirmation endpoint called with data:", data)

        bedsitter_number = data.get("BillRefNumber") # bedsitter number
        amount = float(data.get("TransAmount", 0))
        receipt = data.get("TransID")
        phone = data.get("MSISDN")

        try:
            # Find the bedsitter by number
            bedsitter = Bedsitter.objects.get(number = bedsitter_number)
            print(f"Bedsitter found: {bedsitter_number}")

            # Find the tenant profile living in this bedsitter
            tenant = Tenantprofile.objects.get(bedsitter = bedsitter)
            print(f"Tenant found: {tenant}")

            # Find the first unpaid invoice for this tenant with the matching amount
            invoice  = Invoice.objects.get(tenant=tenant, is_paid=False, amount=amount)
            print(f"Unpaid Invoice found: {invoice}")

            invoice.is_paid = True
            invoice.save()
            print(f"Invoice marked as paid: {invoice}")

            # Record the payment
            Payment.objects.create(
                tenant=tenant,
                invoice=invoice,
                amount=amount,
            )
            print(f"Payment record created for tenant: {tenant}, amount: {amount}")

        except Bedsitter.DoesNotExist:
            # Handle missing bedsitter, tenant, or invoice
            print(f"Bedsitter not found: {bedsitter_number}")
        
        except Tenantprofile.DoesNotExist:
            print(f"Tenant not found for bedsitter: {bedsitter_number}")

        except Invoice.DoesNotExist:
            print(f"Unpaid invoice not found for tenant: {bedsitter_number}, amount: {amount}")

        # Send a success response for M-pesa
        return JsonResponse({"ResultCode":0, "ResultDesc": "Accepted"})
    print("Confirmation endpoint: method not allowed")
    return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
def mpesa_c2b_validation(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body.decode('utf-8'))
        print("Validation endpoint called with data:", data)

        bedsitter_number = data.get("BillRefNumber")  # bedsitter number
        amount = float(data.get("TransAmount", 0))
        receipt = data.get("TransID")
        phone = data.get("MSISDN")

        try:
            # Check if bedsitter exists
            bedsitter = Bedsitter.objects.get(number=bedsitter_number)
            print(f"Bedsitter found: {bedsitter_number}")

            # Check if tenant exists in this bedsitter
            tenant = Tenantprofile.objects.get(bedsitter=bedsitter)
            print(f"Tenant found for bedsitter: {tenant}")

            # Check for an unpaid invoice for this tenant, matching the amount
            invoice = Invoice.objects.get(tenant=tenant, is_paid=False, amount=amount)
            print(f"Unpaid invoice found: {invoice}")

            # If all checks pass, accept the transaction
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
        except Bedsitter.DoesNotExist:
            print(f"Bedsitter not found: {bedsitter_number}")

        except Tenantprofile.DoesNotExist:
            print(f"Tenant not found for bedsitter: {bedsitter_number}")
        
        except Invoice.DoesNotExist:
            print(f"Unpaid invoice not found for tenant: {bedsitter_number}, amount: {amount}")

        # If any check fails, reject the transaction
        print("Validation failed - rejecting transaction")
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Rejected"})
    
    print("Validation endpoint: method not allowed")
    return JsonResponse({"error": "Only POST allowed"}, status=405)