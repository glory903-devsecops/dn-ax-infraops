import os
from .adapter import OpenAIAdapter

class KnowledgeService:
    def __init__(self):
        self.adapter = OpenAIAdapter()
        self.runbook_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'runbook')

    def evolve_runbook(self, event_type, new_insight):
        """
        AI가 기존 런북과 새로운 서술형 인사이트를 결합하여 업데이트된 런북을 생성합니다.
        """
        file_path = os.path.join(self.runbook_dir, f"{event_type}.md")
        
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        prompt = f"""
입력된 '새로운 운영 노하우'를 바탕으로 기존의 '네트워킹 장애 대응 런북'을 지능적으로 업데이트하세요.

[기존 런북 내용]
{original_content}

[새로운 운영 노하우 (서술형)]
{new_insight}

[업데이트 지침]
1. 기존의 Markdown 구조(#, ##, 1., -)를 반드시 유지하세요.
2. 새로운 노하우를 가장 적절한 섹션(예: 예상 원인 분석 또는 표준 조치 프로토콜)에 자연스럽게 통합하거나, '## 📝 Lessons Learned (Auto-Updated)' 섹션을 새로 만들어 추가하세요.
3. 전문적인 IT/인프라 용어를 사용하고 한국어로 작성하세요.
4. 업데이트된 런북의 전체 내용(Markdown 포맷)만 응답하세요.
"""
        # AI 호출 (기존 어댑터 재활용)
        # OpenAIAdapter.generate_analysis는 JSON 파싱을 시도하므로, 
        # 여기서는 텍스트 응답을 직접 받기 위해 어댑터의 핵심 로직을 참고하거나 확장해야 함.
        # 일단은 기존 어댑터를 사용하여 텍스트 결과만 추출하는 방식 시도.
        
        try:
            # 텍스트 응답을 위해 직접 호출 로직 구성 (또는 어댑터 수정 필요)
            import openai
            from dotenv import load_dotenv
            load_dotenv()
            
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {{"role": "system", "content": "너는 숙련된 SRE/네트워크 운영 전문가이며 런북 최적화 전문 AI야."}},
                    {{"role": "user", "content": prompt}}
                ],
                temperature=0.5
            )
            updated_content = response.choices[0].message.content.strip()

            # 파일 업데이트 (실제 반영)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            return updated_content
        except Exception as e:
            print(f"❌ 런북 업데이트 중 오류 발생: {e}")
            return None
