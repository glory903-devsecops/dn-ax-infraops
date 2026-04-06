from django.contrib import admin
from .models import Target, MonitoringLog, Event

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'created_at')

@admin.register(MonitoringLog)
class MonitoringLogAdmin(admin.ModelAdmin):
    list_display = ('target', 'is_available', 'response_time', 'timestamp')
    list_filter = ('target', 'is_available')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('target', 'event_type', 'message', 'is_active', 'created_at')
    list_filter = ('event_type', 'is_active')
