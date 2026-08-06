# backend/routers/convert.py
from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import ConvertRequest, ConvertResponse
from backend.services.tone_converter import ToneConverter

router = APIRouter()

# ToneConverter 인스턴스 생성
try:
    converter = ToneConverter()
except ValueError as e:
    # API 키 누락 등의 예외 발생 시 일단 None으로 처리하고 라우터 호출 시점에서 에러를 던지도록 함
    converter = None

@router.post("/convert", response_model=ConvertResponse)
async def convert_tone(payload: ConvertRequest):
    if not converter:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM API 호출 설정이 준비되지 않았습니다. UPSTAGE_API_KEY를 확인하세요."
        )
    
    if not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="text 필드는 필수이며 1자 이상이어야 합니다."
        )
        
    if payload.target_audience not in ["boss", "colleague", "client", "team"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="target_audience는 'boss', 'colleague', 'client', 'team' 중 하나여야 합니다."
        )

    try:
        converted_text = await converter.convert(payload.text, payload.target_audience)
        return ConvertResponse(
            converted_text=converted_text,
            target_audience=payload.target_audience,
            original_text=payload.text
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM API 호출 중 오류가 발생했습니다: {str(e)}"
        )
