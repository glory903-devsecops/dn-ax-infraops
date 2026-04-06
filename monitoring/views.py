from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Target, MonitoringLog, Event

class DashboardView(TemplateView):
    template_name = 'monitoring/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 13개 사업장 인프라 운영 경험을 반영한 타깃 필터링 또는 요약
        context['targets'] = Target.objects.all()
        context['active_events'] = Event.objects.filter(is_active=True).order_by('-created_at')
        context['uptime_avg'] = 99.98  # PoC용 고정값 또는 계산값
        return context

class TargetStatusView(APIView):
    """실시간 상태 업데이트를 위한 API (AJAX 호출용)"""
    def get(self, request):
        targets = Target.objects.all()
        data = []
        for t in targets:
            latest_log = t.logs.order_by('-timestamp').first()
            data.append({
                'id': t.id,
                'name': t.name,
                'is_available': latest_log.is_available if latest_log else True,
                'response_time': latest_log.response_time if latest_log else 0,
            })
        return Response(data)
