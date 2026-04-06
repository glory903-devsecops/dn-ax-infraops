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
            {'name': 'DN-Cloud-Storage-NAS', 'ip_address': '10.10.20.50', 'description': '글로벌 통합 파일 스토리지 (NetApp)'},
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
            }
        ]
    }

def export():
    # 출력 경로 설정 (docs 폴더)
    dist_dir = os.path.join(settings.BASE_DIR, 'docs')
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)

    # 정적 파일 복사
    static_src = os.path.join(settings.BASE_DIR, 'static')
    static_dst = os.path.join(dist_dir, 'static')
    if os.path.exists(static_dst):
        shutil.rmtree(static_dst)
    shutil.copytree(static_src, static_dst)

    # 렌더링
    context = get_mock_data()
    html_content = render_to_string('monitoring/dashboard.html', context)

    # 1. GitHub Pages 상대 경로 보정
    html_content = html_content.replace('href="/static/', 'href="./static/')
    html_content = html_content.replace('src="/static/', 'src="./static/')

    # 2. 정적 데모용 지식 진화(Evolution) 시뮬레이션 코드 주입
    # 실시간 API 대신 자바스크립트로 지식 업데이트 연출
    simulation_script = """
    async function submitEvolution() {
        const insight = document.getElementById('evolveInsight').value;
        if (!insight.trim()) { alert('지침 내용을 입력해주세요.'); return; }
        
        const btn = event.target;
        btn.disabled = true;
        btn.innerHTML = 'AI 지식 분석 및 통합 중... (시뮬레이션)';
        
        // 지능형 학습 연출을 위한 딜레이
        await new Promise(r => setTimeout(r, 2000));
        
        alert('✨ [AI 지능형 학습 완료]\\n\\n입력하신 노하우를 분석하여 런북 지식 베이스를 v1.1로 업데이트했습니다.\\n\\n추가된 내용: ' + insight.substring(0,30) + '...');
        
        // 화면 레이아웃에 실시간 지식 추가 효과 연출
        const aiPanel = document.querySelector('.glass-card[style*="linear-gradient"]');
        if (aiPanel) {
            const lessonsLearned = document.createElement('div');
            lessonsLearned.style.marginTop = '1.5rem';
            lessonsLearned.style.padding = '1rem';
            lessonsLearned.style.background = 'rgba(16, 185, 129, 0.1)';
            lessonsLearned.style.border = '1px dashed var(--status-ok)';
            lessonsLearned.style.borderRadius = '8px';
            lessonsLearned.innerHTML = '<div style="font-size:0.75rem; font-weight:800; color:var(--status-ok); margin-bottom:0.5rem;">📝 LESSONS LEARNED (AUTO-UPDATED)</div><div style="font-size:0.85rem; color:#e5e7eb;">' + insight + '</div>';
            aiPanel.appendChild(lessonsLearned);
        }
        
        closeEvolveModal();
    }
    """
    # 원본 submitEvolution 함수를 시뮬레이션용으로 교체
    html_content = html_content.split('async function submitEvolution()')[0] + simulation_script + html_content.split('async function submitEvolution()')[1].split('}')[1]

    # 결과 저장
    with open(os.path.join(dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✨ Static Website (with Knowledge Evolution simulation) exported to: {dist_dir}/index.html")

if __name__ == "__main__":
    export()
