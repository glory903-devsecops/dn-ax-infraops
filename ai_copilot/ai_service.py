import os
from .adapter import OpenAIAdapter, InternalLLMAdapter
from .prompt_builder import PromptBuilder
from django.conf import settings

class AICopilotService:
    def __init__(self):
        # 환경 변수에 따라 적절한 어댑터 선택
        provider = os.getenv('LLM_PROVIDER', 'openai')
        api_key = os.getenv('LLM_API_KEY', '')
        
        if provider == 'openai':
            self.adapter = OpenAIAdapter(api_key)
        else:
            self.adapter = InternalLLMAdapter()

    async def analyze_event(self, event):
        # 1. 런북 파일 읽기
        runbook_path = os.path.join(settings.BASE_DIR, 'runbook', f"{event.event_type}.md")
        runbook_content = ""
        if os.path.exists(runbook_path):
            with open(runbook_path, 'r', encoding='utf-8') as f:
                runbook_content = f.read()
        else:
            runbook_content = "해당 장애 유형에 대한 표준 런북이 정의되지 않았습니다."

        # 2. 프롬프트 생성
        builder = PromptBuilder(
            target_name=event.target.name,
            event_type=event.get_event_type_display(),
            message=event.message,
            runbook_content=runbook_content
        )
        prompt = builder.build()

        # 3. LLM 분석 요청
        result = await self.adapter.generate_analysis(prompt)
        
        # 4. 결과 파싱 및 저장 (OpenAI response format)
        try:
            if "choices" in result:
                content = result['choices'][0]['message']['content']
                import json
                analysis_data = json.loads(content)
                return analysis_data
            else:
                return {"error": result.get("error", "Unknown API error")}
        except Exception as e:
            return {"error": f"Parsing error: {str(e)}", "raw": str(result)}
