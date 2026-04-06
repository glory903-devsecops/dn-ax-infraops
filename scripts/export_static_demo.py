import os
import sys
import django
import shutil
from django.template.loader import render_to_string
from django.conf import settings

# 1. Django 가상 환경 설정 (Static Export 전용)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# 2. 데이터 모킹 (Mocking) - DB 연결 없이 정적 페이지를 위해 직접 데이터 구성
def get_mock_data():
    return {
        'uptime_avg': 99.98,
        'targets': [
            {'name': 'DN-HQ-Core-Backbone', 'ip_address': '10.0.0.1', 'description': '서울 본사 코어 백본 스위치 (Nexus 9K)'},
            {'name': 'DN-Factory-CW-Line1', 'ip_address': '172.16.10.1', 'description': '창원 공장 생산 1라인 게이트웨이'},
            {'name': 'DN-Global-Sales-EU', 'ip_address': '192.168.100.5', 'description': '유럽 법인(Germany) 거점 VPN 라우터'},
            {'name': 'DN-R&D-Center-ASIC', 'ip_address': '10.50.0.10', 'description': 'R&D 센터 전용 설계 인프라 노드'},
            {'name': 'DN-Cloud-Bridge-AWS', 'ip_address': '44.200.1.5', 'description': '하이브리드 클라우드 전용 회선 (Direct Connect)'},
        ],
        'active_events': [
            {
                'target': {'name': 'DN-HQ-Core-Backbone'},
                'event_type': 'LINK_DOWN',
                'message': 'Interface Ethernet 1/1 (Primary) is DOWN. Protocol status down.',
                'copilot_analysis': {
                    "summary": "DN-HQ-Core-Backbone에서 주 회선(Primary) 단절이 감지되어 백업 회선으로 자동 Failover 중입니다.",
                    "causes": ["외부 광케이블 굴착 공사 물리적 단절", "SFP 모듈 하드웨어 결함"],
                    "recommended_actions": [
                        "Cisco 'show interface status' 명령어로 포트 상태 확인",
                        "통신사(KT) 글로벌 회선 장애 센터 티켓 오픈 확인",
                        "백업 트래픽 점유율 모니터링"
                    ]
                }
            },
            {
                'target': {'name': 'DN-Factory-CW-Line1'},
                'event_type': 'LATENCY_HIGH',
                'message': 'Average RTT: 452ms. Threshold: 200ms.',
                'copilot_analysis': {
                    "summary": "창원 공장 생산 1라인 게이트웨이의 지연 시간이 임계치를 초과하였습니다.",
                    "causes": ["생산 라인 센서 데이터 폭증", "네트워크 루프 발생 의심"],
                    "recommended_actions": [
                        "L2 스위치 MAC 플래핑 여부 체크",
                        "의심되는 포트에 트래픽 셰이핑 적용"
                    ]
                }
            }
        ]
    }

def export():
    # 출력 경로 설정 (GitHub Pages용 docs 폴더 - main 브랜치 배포용)
    dist_dir = os.path.join(settings.BASE_DIR, 'docs')
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)

    # 정적 파일 복사 (CSS, JS 등)
    static_src = os.path.join(settings.BASE_DIR, 'static')
    static_dst = os.path.join(dist_dir, 'static')
    if os.path.exists(static_dst):
        shutil.rmtree(static_dst)
    shutil.copytree(static_src, static_dst)

    # 렌더링 (Context 데이터 전달)
    context = get_mock_data()
    html_content = render_to_string('monitoring/dashboard.html', context)

    # GitHub Pages용 상대 경로 보정 ( /static/ -> ./static/ )
    html_content = html_content.replace('href="/static/', 'href="./static/')
    html_content = html_content.replace('src="/static/', 'src="./static/')

    # 결과 저장
    with open(os.path.join(dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✨ Static Website exported to: {dist_dir}/index.html")

if __name__ == "__main__":
    export()
