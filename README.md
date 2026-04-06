# 🚀 DN Solutions | InfraOps Copilot (Demo)

[![Deploy to GitHub Pages](https://github.com/glory903-devsecops/dn-ax-infraops/actions/workflows/deploy.yml/badge.svg)](https://github.com/glory903-devsecops/dn-ax-infraops/actions/workflows/deploy.yml)

> **"지능형 런북 기반의 글로벌 인프라 장애 대응 자동화 플랫폼"**  
> **[👉 실시간 데모 사이트 바로가기](https://glory903-devsecops.github.io/dn-ax-infraops/)**

본 프로젝트는 **DN 솔루션즈**의 글로벌 인프라 운영 효율성을 극대화하기 위해 설계된 AI 기반의 Intelligent Monitoring & Operations PoC입니다.

---

## 📈 핵심 가치 (Core Values)

1.  **AI 기반 장애 원인 분석**: 수천 페이지의 물리적 런북(Runbook)을 AI가 실시간으로 학습하여 대응 매뉴얼을 즉시 제시합니다.
2.  **표준화된 운영 (ITIL/SRE)**: 글로벌 표준(ITIL, Cisco, SRE)에 기반한 데이터 중심의 인프라 운영 체계를 제안합니다.
3.  **GitHub Actions 자동 배포**: CI/CD 파이프라인을 통한 정적 데모 사이트 배포로 실시간 가시성을 확보합니다.

## 📡 인프라 시나리오 (DN Solutions Focus)

-   **DN-HQ-Core-Backbone**: 서울 본사 L3 코어 인프라 (Nexus 9K)
-   **DN-Factory-CW-Line1**: 창원 공장 MES 연동 생산 라인 게이트웨이
-   **DN-Global-Sales-EU**: 유럽 법인(Germany) 거점 VPN 라우터
-   **DN-Cloud-Bridge-AWS**: 하이브리드 클라우드 전용 회선(Direct Connect)

---

## 🛠️ 주요 기술 스택

-   **Backend**: Python / Django 4.2
-   **AI Engine**: OpenAI GPT-4o Integration
-   **Deployment**: GitHub Actions + GitHub Pages (Static Portfolio)
-   **UI/UX**: Vanilla CSS Premium Dashboard (Glassmorphism)

---

## 🚀 빠른 시작 (Quick Start)

본 프로젝트는 Docker 환경에서 즉시 실행하거나, 위의 데모 링크를 통해 즉시 확인할 수 있습니다.

```bash
# 1. 프로젝트 실행 (로컬 환경)
docker-compose up --build -d

# 2. 실전형 데모 데이터 주입
docker-compose exec web python scripts/populate_dn_demo.py

# 3. 로컬 대시보드 접속
http://localhost:8000
```

---
*Created by [사용자 성함/ID] - DN Solutions Infra Operations Professional Portfolio*
