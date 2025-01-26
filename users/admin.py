from django.contrib import admin

from .models import Administrator, HealthPersonnel


@admin.action(description='Archive selected professionals')
def archive(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.action(description='Restore selected professionals')
def restore(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.register(HealthPersonnel)
class HealthPersonnelAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'first_name', 'last_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['employee_id', 'first_name', 'last_name']
    actions = [archive, restore]

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'first_name', 'last_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['employee_id', 'first_name', 'last_name']
    actions = [archive, restore]