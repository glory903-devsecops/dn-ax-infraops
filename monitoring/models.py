from django.db import models

class Target(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.ip_address})"

class MonitoringLog(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='logs')
    is_available = models.BooleanField(default=True)
    response_time = models.FloatField(null=True, blank=True) # in ms
    status_code = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    EVENT_TYPES = [
        ('LINK_DOWN', 'Link Down'),
        ('LATENCY_HIGH', 'Latency High'),
        ('PACKET_LOSS', 'Packet Loss'),
        ('DNS_ISSUE', 'DNS Issue'),
    ]
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # AI Analysis
    copilot_analysis = models.JSONField(null=True, blank=True) # {summary, causes, checklist, recommended_actions}
