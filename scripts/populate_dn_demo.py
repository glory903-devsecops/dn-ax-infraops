import os
import sys
import django
from django.utils import timezone

# Django 환경 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from monitoring.models import Target, Event, MonitoringLog

def populate():
    print("🔩 [DN Solutions] 인텔리전트 인프라 데모 데이터 구축 시작...")

    # 1. 기존 데이터 정리 (Clean up for a fresh demo)
    Target.objects.all().delete()
    Event.objects.all().delete()

    # 2. 실전형 DN 솔루션즈 타깃 생성 (HQ, Factory, Global Site)
    targets_data = [
        {'name': 'DN-HQ-Core-Backbone', 'ip': '10.0.0.1', 'desc': '서울 본사 코어 백본 스위치 (Nexus 9K)'},
        {'name': 'DN-Factory-CW-Line1', 'ip': '172.16.10.1', 'desc': '창원 공장 생산 1라인 게이트웨이'},
        {'name': 'DN-Global-Sales-EU', 'ip': '192.168.100.5', 'desc': '유럽 법인(Germany) 거점 VPN 라우터'},
        {'name': 'DN-R&D-Center-ASIC', 'ip': '10.50.0.10', 'desc': 'R&D 센터 전용 설계 인프라 노드'},
        {'name': 'DN-Cloud-Bridge-AWS', 'ip': '44.200.1.5', 'desc': '하이브리드 클라우드 전용 회선 (Direct Connect)'},
    ]

    targets = []
    for t_data in targets_data:
        t = Target.objects.create(
            name=t_data['name'],
            ip_address=t_data['ip'],
            description=t_data['desc']
        )
        targets.append(t)
        print(f"✅ 타깃 생성: {t.name}")

    # 3. 사전 생성된 '전문가급 AI 분석' 장애 이벤트 (Demo Ready)
    # 3.1 LINK_DOWN - 본사 백본 이슈
    analysis_link = {
        "summary": "DN-HQ-Core-Backbone에서 주 회선(Primary) 단절이 감지되었습니다. 현재 백업 회선으로 자동 Failover된 상태이나, 처리량(Throughput) 저하가 예상됩니다.",
        "causes": [
            "창원 국사 인근 외부 광케이블 굴착 공사로 인한 물리적 단절 유력",
            "SFP 모듈(Transceiver) 하드웨어 결함",
            "최근 백본 스위치 펌웨어 업데이트 이후 인터페이스 불안정성"
        ],
        "checklist": [
            "Cisco `show interface status` 명령어로 포트 'Error-Disabled' 여부 확인",
            "통신사(KT) 글로벌 회선 장애 센터(NOC) 티켓 오픈 유무 확인",
            "백업 라인(Secondary)의 트래픽 점유율(Utilization) 모니터링"
        ],
        "recommended_actions": [
            "현장 담당자 협조를 통한 물리적 포트 광신호(Rx/Tx) 세기 측정",
            "장애 지속 시 비업무용 트래픽(Cloud Sync 등) 일시 차단하여 가용성 확보",
            "펌웨어 롤백 준비 및 유지보수 파트너사 긴급 호출"
        ],
        "urgency": "Critical"
    }

    Event.objects.create(
        target=targets[0],
        event_type='LINK_DOWN',
        message="Interface Ethernet 1/1 (Primary) is DOWN. Protocol status down.",
        copilot_analysis=analysis_link,
        is_active=True
    )

    # 3.2 LATENCY_HIGH - 창원 공장 라인 이슈
    analysis_lat = {
        "summary": "창원 공장 생산 1라인 게이트웨이의 지연 시간이 임곗값(200ms)을 초과하여 450ms에 도달했습니다.",
        "causes": [
            "생산 라인 센서 데이터 폭증으로 인한 버퍼 오버플로우",
            "특정 노드에서의 ARP 스푸핑 또는 네트워크 루프 발생 의심",
            "공장 내 무선 AP(Mesh) 간섭으로 인한 패킷 지연"
        ],
        "checklist": [
            "L2 스위치에서 `show mac address-table` 확인하여 MAC 플래핑 여부 체크",
            "QoS 정책이 생산 장비 트래픽을 정상적으로 보장하고 있는지 확인"
        ],
        "recommended_actions": [
            "의심되는 포트에 대한 트래픽 셰이핑(Shaping) 강화",
            "현장 AP 채널 최적화 및 고정 채널 할당 검토",
            "생산 관리 시스템(MES)과의 데이터 전송 로그 교차 검증"
        ],
        "urgency": "High"
    }

    Event.objects.create(
        target=targets[1],
        event_type='LATENCY_HIGH',
        message="Average RTT: 452ms. Threshold: 200ms.",
        copilot_analysis=analysis_lat,
        is_active=True
    )

    print("✨ [DN Solutions] 데모용 전문 데이터 구축이 완료되었습니다!")

if __name__ == "__main__":
    populate()
