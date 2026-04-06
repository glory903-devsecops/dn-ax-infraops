# 🏗️ InfraOps Copilot Architecture Design

본 문서는 **InfraOps Copilot**의 주요 설계 결정 사항과 아키텍처 구조를 설명합니다.

---

## 1. AI Integration Strategy: Adapter Pattern
다양한 LLM API(OpenAI, Gemini, 사내 모델 등)를 유연하게 지원하기 위해 **Adapter Pattern**을 적용했습니다.

- **인터페이스 (`LLMAdapter`)**: 모든 AI 공급자가 준수해야 할 추상 메서드를 정의합니다.
- **공급자 구현 (`OpenAIAdapter`, `InternalLLMAdapter`)**: 구체적인 API 호출 로직을 캡슐화합니다.
- **장점**: 특정 모델에 대한 의존도(Vendor Lock-in)를 낮추고, 향후 더 비용 효율적이거나 성능이 좋은 모델로의 즉각적인 전환이 가능합니다.

## 2. Intelligence Logic: Runbook-based RAG
단순한 AI 채팅이 아닌, **표준 운영 절차(SOP)**를 기반으로 한 상황별 응대 가이드를 생성하기 위해 RAG(Retrieval-Augmented Generation) 개념을 응용했습니다.

1.  **Context Aggregation**: 장애가 발생한 `Target`의 실시간 메트릭 정보를 수집합니다.
2.  **Knowledge Retrieval**: 장애 유형에 매핑된 Markdown 형식의 **Runbook** 내용을 읽어옵니다.
3.  **Prompt Engineering**: 수집된 데이터와 Runbook 지식을 결합하여 최적화된 프롬프트를 생성합니다.
4.  **Structured JSON Output**: AI로부터 비정형 텍스트가 아닌, **구조화된 JSON 데이터**를 받아 대시보드 UI에 즉시 시각화합니다.

## 3. Monitoring & Event Workflow
모니터링 데이터가 장애로 이어지는 과정은 다음과 같이 설계되었습니다.

- **Check Engine**: ICMP/Ping 또는 HTTP 상태를 주기적으로 체크합니다.
- **Event Dispatcher**: 장애 임곗값 도달 시 `Event` 모델을 생성하고 `AICopilotService`를 통합 호출합니다.
- **Asynchronous Execution**: AI 분석은 네트워크 지연이 발생할 수 있는 작업이므로, 비동기 처리를 기본으로 하여 대시보드 반응 속도를 유지합니다.

## 4. UI/UX Concept: High-Tech Enterprise
**DN 솔루션즈**의 신뢰성과 혁신을 상징하기 위해 **DN Blue (#005EBB)**를 핵심 테마로 사용했습니다.

- **Dark Mode**: 야간 관제 상황을 고려한 고대비 테마.
- **Glassmorphism**: 카드형 레이아웃에 투명도와 블러 효과를 적용하여 현대적인 엔지니어링 룩 구현.
- **Visual Feedback**: 장애 발생 시 맥박(Pulse) 애니메이션과 선명한 컬러 인디케이터를 통해 가시성 확보.

---
*Design by Antigravity for the Global Infra Ops Excellence.*
