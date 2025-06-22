from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.admin_dashboard, name='index'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('apartments/', views.apartments_list, name='apartments_list'),
    path('bedsitters/', views.bedsitters_list, name='bedsitters_list'),
    path('apartments/<int:apartment_id>/bedsitters/', views.apartment_bedsitters, name='apartment_bedsitters'),
    path('tenantprofiles/apartment/<int:apartment_id>/', views.tenantprofiles_by_apartment, name='tenantprofiles_by_apartment'),
    path('payment/c2b/confirmation/', views.mpesa_c2b_confirmation, name='mpesa_c2b_confirmation'),
    path('payment/c2b/validation/', views.mpesa_c2b_validation, name='mpesa_c2b_validation'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('payments/', views.payment_list, name='payment_list'),
    path('receipts/', views.receipt_list, name='receipt_list'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add-tenant/', views.add_tenant, name='add_tenant'),
    path('add-user/', views.add_user, name='add_user'),
]