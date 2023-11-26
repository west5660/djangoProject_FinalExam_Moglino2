from django.contrib import admin
from .models import UserProfile, ServiceType, Service, Order


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization_name', 'production_type', 'project_status', 'phone_number', 'email')


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'unit_of_measurement', 'cost', 'note', 'provider')
    list_filter = ('service_type', 'provider')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'quantity', 'total_cost')
    list_filter = ('user', 'service')
