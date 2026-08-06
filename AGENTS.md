# 💼 업무 말투 변환기 — AGENTS.md

이 파일은 **Google Antigravity** 에이전트가 본 프로젝트("업무 말투 변환기")를 개발 및 검증할 때 반드시 준수해야 하는 **규칙(Rules)**과 **프로젝트 개요**를 정의한 문서입니다. 에이전트는 작업을 시작하기 전에 이 문서를 읽고 규칙을 내재화해야 합니다.

---

## 1. 프로젝트 개요 (Project Overview)

**업무 말투 변환기**는 사용자가 일상적인 말투로 작성한 문장을 입력하면, AI(Upstage Solar-Pro3)를 통해 수신 대상(상사, 동료, 고객 등)에 최적화된 정중하고 적절한 비즈니스 말투로 변환해 주는 서비스입니다.

- **목표**: 일체 불필요한 기능(로그인, DB 저장, 이력 관리 등)을 제외하고, 핵심 말투 변환 기능을 완벽하게 작동하도록 구현합니다.
- **주요 기술**: HTML/CSS/Vanilla JS (프론트엔드) + Python FastAPI (백엔드) + LangChain & Upstage Solar-Pro3 API (AI 모델)

---

## 2. 에이전트 준수 규칙 (Agent Rules)

### ⚠️ [바이브 코딩 3원칙] 절대 준수
1. **완료 기준을 먼저 정의하라**: 임의로 기능을 추가하거나 변형하지 말고, 하단의 **[완료 체크리스트]** 항목 충족에만 집중하십시오.
2. **조사 먼저, 구현 나중**: Solar-Pro3 API 연동이나 패키지 구조 등 외부 요소를 사용하기 전 반드시 문서를 사전 검토하고, 올바른 연동법을 인지한 상태에서 코드를 작성하십시오.
3. **버그는 분석 먼저, 수정 나중**: 에러가 발생하면 임의로 코드를 수정해 누더기로 만들지 말고, 원인을 먼저 분석하여 설명한 뒤 근본적인 해결책으로 수정하십시오.

### 🔒 [보안 및 안전 수칙]
- `.env` 파일은 절대 외부로 노출하거나 커밋하지 말고, `.gitignore`에 등록되어 있는지 반드시 확인하십시오.
- 민감 정보가 포함될 수 있는 파일 수정 시 [글로벌 시스템 지침]에 지정된 파괴적 행동 방지 수칙을 철저히 지키십시오.

---

## 3. 디렉토리 구조 (Directory Structure)

에이전트는 아래의 디렉토리 및 파일 구조를 그대로 유지하며 개발을 진행해야 합니다.

```
biztalk_antigravity/
├── .venv/                      # 가상환경
├── backend/
│   ├── main.py                 # FastAPI 앱 + CORS 및 라우터 설정
│   ├── routers/
│   │   └── convert.py          # /api/convert 라우터 구현
│   ├── services/
│   │   └── tone_converter.py   # LangChain + Solar-Pro3 연동 핵심 로직
│   ├── prompts/
│   │   └── templates.py        # 수신 대상별(boss, colleague, client, team) 프롬프트 템플릿
│   ├── models/
│   │   └── schemas.py          # Pydantic 요청/응답 스키마
│   └── requirements.txt        # 백엔드 의존성 목록
│
├── frontend/
│   ├── index.html              # 메인 UI 레이아웃 (Vanilla HTML)
│   ├── css/
│   │   └── style.css           # UI 스타일링 (Vanilla CSS)
│   └── js/
│       └── app.js              # API 호출 및 화면 갱신 로직 (Vanilla JS)
│
├── .env                        # API 키 보관용 환경변수 파일 (Git 제외 대상)
├── .gitignore                  # Git 제외 설정
├── PRD_업무말투변환기.md        # 상세 PRD
└── 개요서_업무말투변환기.md    # 프로젝트 개요서
```

---

## 4. 완료 체크리스트 (Definition of Done)

작업 완료 여부를 판정하기 위한 체크리스트입니다. 에이전트는 작업을 마무리할 때 각 항목이 실제로 구현되고 검증되었는지 교차 검증해야 합니다.

### 백엔드 (FastAPI)
- [ ] FastAPI 서버가 로컬에서 오류 없이 정상 실행된다 (`uvicorn main:app`).
- [ ] `/health` (Health Check) API가 존재하며 `{ "status": "ok" }`를 반환한다.
- [ ] `POST /api/convert` 엔드포인트가 정상 작동한다.
- [ ] `UPSTAGE_API_KEY`를 `.env`를 통해 안전하게 로드하고, Upstage Solar-Pro3 API를 정상적으로 호출한다.
- [ ] 수신 대상(상사, 타팀 동료, 고객, 팀 내 동료) 4종 각각에 대하여 다르게 매핑된 프롬프트가 적용된다.
- [ ] 프론트엔드 연동을 위해 CORS 미들웨어가 적절하게 설정되어 있다.
- [ ] Swagger UI(`/docs`)를 통해 API 브라우징 및 테스트가 가능하다.

### 프론트엔드 (UI & UX)
- [ ] 사용자가 원문을 입력할 수 있는 텍스트 입력창이 존재한다.
- [ ] 4종의 수신 대상을 토글 선택할 수 있는 버튼 UI가 제공되며, 한 번에 하나만 활성화(Active)된다.
- [ ] [변환하기] 버튼 클릭 시 API 호출을 트리거하며, API 로딩 시 사용자에게 시각적인 로딩 표시가 나타난다.
- [ ] 변환이 완료되면 결과 창에 텍스트가 출력된다.
- [ ] [복사하기] 버튼이 정상 작동하여 변환 결과 텍스트가 클립보드에 복사된다.
- [ ] Web Application Development 가이드라인에 따라 화면이 시각적으로 미려하고 트렌디하게 디자인된다 (Premium/Rich Aesthetics).

### 배포 및 검증
- [ ] 소스 코드가 Git 저장소에 정돈된 구조로 안전하게 추적되어 있다.
- [ ] 로컬 실행 및 원격 배포 준비 상태가 완료되었다.
