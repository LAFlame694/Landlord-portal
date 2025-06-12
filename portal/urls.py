from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='index'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('tenant-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('apartments/', views.apartments_list, name='apartments_list'),
    path('bedsitters/', views.bedsitters_list, name='bedsitters_list'),
    path('apartments/<int:apartment_id>/bedsitters/', views.apartment_bedsitters, name='apartment_bedsitters'),
    path('tenantprofiles/apartment/<int:apartment_id>/', views.tenantprofiles_by_apartment, name='tenantprofiles_by_apartment'),
    path('payment/c2b/confirmation/', views.mpesa_c2b_confirmation, name='mpesa_c2b_confirmation'),
    path('payment/c2b/validation/', views.mpesa_c2b_validation, name='mpesa_c2b_validation'),
]