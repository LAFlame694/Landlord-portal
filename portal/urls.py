from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='index'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('tenant-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('apartments/', views.apartments_list, name='apartments_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bedsitters/', views.bedsitters_list, name='bedsitters_list')
]