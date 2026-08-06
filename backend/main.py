import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from backend.routers import convert

app = FastAPI(
    title="BizTalk Antigravity API",
    description="일상적인 표현을 정중한 비즈니스 말투로 자동 변환하는 API 서비스",
    version="1.0.0"
)

# CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production code should restrict this to target domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check API
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# API router inclusions
app.include_router(convert.router, prefix="/api", tags=["Convert"])

# Static Files serving for Frontend (at the very bottom to avoid routing conflicts)
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

