from typing import Dict, Any

class PromptBuilder:
    def __init__(self, target_name: str, event_type: str, message: str, runbook_content: str):
        self.target_name = target_name
        self.event_type = event_type
        self.message = message
        self.runbook_content = runbook_content

    def build(self) -> str:
        prompt = f"""
당신은 DN 솔루션즈의 글로벌 인프라 운영을 지원하는 전문 'InfraOps Copilot'입니다.
다음 발생한 장애 이벤트와 해당 시나리오의 표준 Runbook(SOP)을 참고하여 상황을 분석하고 대응 가이드를 생성하십시오.

[장애 정보]
- 대상: {self.target_name} (Global Infrastructure Node)
- 이벤트 유형: {self.event_type}
- 상세 메시지: {self.message}

[참고 Runbook (표준 운영 절차)]
{self.runbook_content}

[요구사항]
아래 JSON 형식으로 응답하십시오:
1. summary: 상황 요약 (1~2줄)
2. causes: 유력한 원인 후보 (우선순위 순 리스트)
3. checklist: 관리자가 즉시 확인해야 할 체크리스트 (명령어 포함 권장)
4. recommended_actions: 구체적인 조치 단계 (우선순위 순 리스트)
5. urgency: 긴급도 (Low/Medium/High/Critical)

응답은 반드시 한국어로 작성하십시오.
"""
        return prompt
