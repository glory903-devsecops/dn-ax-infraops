import os
import sys
import django
import asyncio
from asgiref.sync import sync_to_async

# Django 환경 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from monitoring.models import Target, Event
from ai_copilot.ai_service import AICopilotService

async def simulate(scenario_type, target_name):
    print(f"🚀 [Simulation] {scenario_type} 발생 시연 시작: {target_name}")
    
    # 1. 타깃 확인 및 생성 (Sync ORM to Async)
    target, created = await sync_to_async(Target.objects.get_or_create)(
        name=target_name,
        defaults={'ip_address': '172.16.42.105', 'description': 'DN 글로벌 생산라인 1호기 게이트웨이'}
    )
    if created:
        print(f"✅ 새 타깃 생성: {target_name}")

    # 2. 장애 이벤트 생성
    messages = {
        'LINK_DOWN': "ICMP 도달 불가능 (Unreachable) - 주 회선 단절 감지",
        'LATENCY_HIGH': "평균 응답 속도 450ms 초과 - 로컬 구간 병목 현상",
        'PACKET_LOSS': "패킷 손실률 12% 발생 - 데이터 정합성 위험",
        'DNS_ISSUE': "도메인 resolution 실패 - 본사 DNS 서버 응답 없음",
    }
    
    event = await sync_to_async(Event.objects.create)(
        target=target,
        event_type=scenario_type,
        message=messages.get(scenario_type, "알 수 없는 시스템 장애"),
        is_active=True
    )
    print(f"⚠️  이벤트 로그 저장 완료 (ID: {event.id})")

    # 3. AI Copilot 분석 트리거 (Runbook 기반)
    print("🤖 AI Copilot 분석 중 (Runbook 참조)...")
    service = AICopilotService()
    
    # 실제 AI 호출 시도 (Error 발생 시 모킹 데이터 사용)
    analysis = await service.analyze_event(event)
    
    if "error" in analysis:
        print(f"💡 [Error] AI 분석 중 오류 발생: {analysis['error']}")
        # Fallback Mock Data
        analysis_mock = {
            'summary': f"{target_name}의 주 회선 단절이 감지되었습니다. 현재 외부 ISP(SKB) 구간 장애가 유력합니다.",
            'causes': ["ISP 전용회선 점검 중", "로컬 L3 스위치 SFP 모듈 결함"],
            'checklist': ["show interface status 확인", "회선사 장애 접수 확인"],
            'recommended_actions': ["백업 회선 전환 여부 확인", "케이블 점검"]
        }
        event.copilot_analysis = analysis_mock
    else:
        print("✅ AI 분석 데이터 수신 성공!")
        event.copilot_analysis = analysis
    
    await sync_to_async(event.save)()
    print(f"✨ AI 분석 결과 업데이트 완료! 대시보드에서 확인하십시오.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="InfraOps Copilot 장애 시물레이션")
    parser.add_argument("--scenario", default="LINK_DOWN", help="장애 유형")
    parser.add_argument("--target", default="dn-factory-line-1", help="대상 타깃 명칭")
    
    args = parser.parse_args()
    asyncio.run(simulate(args.scenario, args.target))
