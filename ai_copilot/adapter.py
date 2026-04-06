import abc
import os
import httpx
from typing import Dict, Any

class LLMAdapter(abc.ABC):
    @abc.abstractmethod
    async def generate_analysis(self, prompt: str) -> Dict[str, Any]:
        pass

class OpenAIAdapter(LLMAdapter):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"

    async def generate_analysis(self, prompt: str) -> Dict[str, Any]:
        # .env에서 모델명을 가져오거나 없으면 기본값 사용
        model_name = os.getenv('OPENAI_MODEL', 'gpt-4o')
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "당신은 DN 솔루션즈의 숙련된 InfraOps 전문 AI입니다. 응답은 항상 JSON 형식이어야 합니다."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.api_url, headers=headers, json=payload, timeout=30.0)
                if response.status_code != 200:
                    return {"error": f"API Error {response.status_code}: {response.text}"}
                return response.json()
            except Exception as e:
                return {"error": f"Connection Error: {str(e)}"}

class InternalLLMAdapter(LLMAdapter):
    """사내 LLM 연동을 위한 인터페이스 샘플"""
    async def generate_analysis(self, prompt: str) -> Dict[str, Any]:
        return {"summary": "Internal LLM Mock Analysis", "message": "사내 API 연동 필요"}
