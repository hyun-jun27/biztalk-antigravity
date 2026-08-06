from fastapi import APIRouter, HTTPException, Depends
from backend.models.schemas import ConvertRequest, ConvertResponse
from backend.services.tone_converter import ToneConverter

router = APIRouter()

# Dependency injection for ToneConverter
def get_tone_converter():
    return ToneConverter()

@router.post("/convert", response_model=ConvertResponse)
async def convert_tone(
    request: ConvertRequest,
    converter: ToneConverter = Depends(get_tone_converter)
):
    try:
        converted_text = converter.convert(
            text=request.text,
            target_audience=request.target_audience
        )
        return ConvertResponse(
            converted_text=converted_text,
            target_audience=request.target_audience,
            original_text=request.text
        )
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"LLM API 호출 중 오류가 발생했습니다: {str(exc)}"
        )
