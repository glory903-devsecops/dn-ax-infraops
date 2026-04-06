from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Target, MonitoringLog, Event
from ai_copilot.knowledge_service import KnowledgeService

class DashboardView(TemplateView):
    template_name = 'monitoring/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 13개 사업장 인프라 운영 경험을 반영한 타깃 필터링 또는 요약
        context['targets'] = Target.objects.all()
        # AI 분석 이력이 있는 활성 이벤트만 전달
        context['active_events'] = Event.objects.filter(is_active=True).order_by('-created_at')
        context['uptime_avg'] = 99.98  # PoC용 고정값
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

class UpdateRunbookAPI(APIView):
    """사용자 피드백을 기반으로 런북 지식을 지능적으로 업데이트하는 API"""
    def post(self, request):
        event_type = request.data.get('event_type')
        new_insight = request.data.get('insight')
        
        if not event_type or not new_insight:
            return Response({"error": "사건 유형과 지침 내용을 모두 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        ks = KnowledgeService()
        updated_content = ks.evolve_runbook(event_type, new_insight)
        
        if updated_content:
            return Response({
                "message": f"{event_type} 런북 지식이 지능적으로 업데이트되었습니다.",
                "updated_content": updated_content
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "런북 파일을 찾을 수 없거나 업데이트 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
