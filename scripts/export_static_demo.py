import os
import sys
import django
import shutil
import random
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta

# 1. Django 가상 환경 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def get_mock_data():
    # 1. 1,000개 자산 데이터 생성
    locations = ["서울 본사(HQ)", "창원 1공장", "창원 2공장", "미국 법인(USA)", "독일 법인(Germany)", "중국 법인(China)", "인도 법인(India)"]
    asset_types = ["Core Switch", "L3 Switch", "L2 Edge", "Firewall", "Router", "VPN Gateway", "Storage NAS"]
    statuses = ["NORMAL", "NORMAL", "NORMAL", "NORMAL", "NORMAL", "WARNING", "DOWN"] # 확률적 상태 부여
    
    targets = []
    for i in range(1, 1001):
        loc = random.choice(locations)
        atype = random.choice(asset_types)
        status = random.choice(statuses)
        ip = f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        
        targets.append({
            'name': f"DN-{loc[:2]}-{atype[:3]}-{i:04d}",
            'ip_address': ip,
            'description': f"{loc} 소속 {atype} 자산 (Node-{i})",
            'status': status
        })

    # 2. 최근 활성 이벤트 (대시보드 사이드바용 - 최대 3개)
    active_events = [
        {
            'id': 1001,
            'target': {'name': 'DN-HQ-Core-0051'},
            'event_type': 'LINK_DOWN',
            'message': 'Interface Ethernet 1/1 (Primary) is DOWN.',
            'created_at': datetime.now(),
            'copilot_analysis': {
                "summary": "DN 본사 코어 스위치 1번 포트 단절 감지. 백업 회선으로 자동 Failover가 진행 중입니다.",
                "causes": ["외부 광케이블 물리적 손상 의심", "SFP 모듈 장애"],
                "recommended_actions": ["Cisco Port-Status 대조", "통신사 선로 점검 티켓 요청"]
            }
        },
        {
            'id': 1002,
            'target': {'name': 'DN-창원-L3-0124'},
            'event_type': 'LATENCY_HIGH',
            'message': 'Average Latency > 300ms detected.',
            'created_at': datetime.now() - timedelta(minutes=15),
            'copilot_analysis': {
                "summary": "창원 1공장 L3 스위치 응답 지연 발생. 특정 포트의 트래픽 폭증이 감지되었습니다.",
                "causes": ["네트워크 루프 발생", "대역폭 점유율 임계치 초과"],
                "recommended_actions": ["L2 MAC 플래핑 확인", "Storm Control 설정 임시 적용"]
            }
        },
        {
            'id': 1003,
            'target': {'name': 'DN-USA-VPN-0008'},
            'event_type': 'SECURITY_AUTH_FAIL',
            'message': 'Multiple failed login attempts from 203.0.113.5',
            'created_at': datetime.now() - timedelta(minutes=45),
            'copilot_analysis': {
                "summary": "미국 법인 VPN 게이트웨이에 대한 무차별 대입 공격 의심 징후가 포착되었습니다.",
                "causes": ["외부 IP 무차별 대입(Brute Force)", "유출된 계정 정보 사용 시도"],
                "recommended_actions": ["해당 IP 방화벽 차단 리스트 등록", "2단계 인증 강제 적용 검토"]
            }
        }
    ]

    # 3. 과거 AI 분석 레포트 히스토리 (20개 이상)
    report_history = []
    for i in range(1, 26):
        date = datetime.now() - timedelta(days=i, hours=random.randint(1, 23))
        report_history.append({
            'id': i,
            'date': date.strftime("%Y-%m-%d %H:%M"),
            'target_name': f"DN-OLD-NODE-{i:03d}",
            'event_type': random.choice(['LINK_DOWN', 'TEMP_HIGH', 'CPU_SPIKE', 'BGP_FLAP']),
            'summary': f"AI 분석 레포트 #{i}: 해당 노드의 자산 안정성 검토 및 조치가 완료되었습니다.",
            'status': 'RESOLVED'
        })

    return {
        'uptime_avg': 99.98,
        'managed_nodes_count': 1024,
        'targets': targets,
        'active_events': active_events,
        'report_history': report_history
    }

def export():
    dist_dir = os.path.join(settings.BASE_DIR, 'docs')
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)

    # 정적 파일 복사
    static_src = os.path.join(settings.BASE_DIR, 'static')
    static_dst = os.path.join(dist_dir, 'static')
    if os.path.exists(static_dst):
        shutil.rmtree(static_dst)
    shutil.copytree(static_src, static_dst)

    context = get_mock_data()

    # 1. Dashboard (index.html) 추출
    html_dashboard = render_to_string('monitoring/dashboard.html', context)
    html_dashboard = html_dashboard.replace('href="/static/', 'href="./static/')
    html_dashboard = html_dashboard.replace('src="/static/', 'src="./static/')
    # URL 보정: reports.html로 연결되도록
    html_dashboard = html_dashboard.replace('href="/reports/"', 'href="./reports.html"')
    
    with open(os.path.join(dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_dashboard)

    # 2. AI Report List (reports.html) 추출
    html_reports = render_to_string('monitoring/report_list.html', context)
    html_reports = html_reports.replace('href="/static/', 'href="./static/')
    html_reports = html_reports.replace('src="/static/', 'src="./static/')
    # Dashboard로 돌아오기 링크 보정
    html_reports = html_reports.replace('href="/"', 'href="./index.html"')
    
    with open(os.path.join(dist_dir, 'reports.html'), 'w', encoding='utf-8') as f:
        f.write(html_reports)

    print(f"✨ Static Website (Dashboard & Reports) exported to: {dist_dir}")

if __name__ == "__main__":
    export()
