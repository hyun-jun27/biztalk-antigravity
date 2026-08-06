# backend/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.routers import convert

app = FastAPI(
    title="BizTalk Antigravity API",
    description="업무 말투 변환기 API 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 시 실제 도메인으로 변경 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(convert.router, prefix="/api")

# Health Check 기능
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 프론트엔드 정적 파일 서빙 설정
# backend 디렉토리를 기준으로 frontend 디렉토리의 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

# css, js 디렉토리가 존재하는 경우 정적 파일 마운트
if os.path.exists(FRONTEND_DIR):
    # 루트 / 접근 시 index.html 서빙
    @app.get("/")
    async def serve_index():
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "index.html이 존재하지 않습니다."}

    # frontend 폴더 전체를 정적으로 제공하되, css/js 하위 정적 파일을 서빙할 수 있도록 설정
    app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="frontend")
