# backend/services/tone_converter.py
import os
from dotenv import load_dotenv
from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from backend.prompts.templates import PROMPTS

# .env 파일 로드
load_dotenv()

class ToneConverter:
    def __init__(self):
        # UPSTAGE_API_KEY 확인
        api_key = os.getenv("UPSTAGE_API_KEY")
        if not api_key:
            raise ValueError("UPSTAGE_API_KEY가 환경 변수나 .env 파일에 설정되어 있지 않습니다.")
        
        # langchain-upstage를 활용하여 ChatUpstage 초기화
        # 모델은 solar-pro3를 사용
        self.llm = ChatUpstage(model="solar-pro3")

    async def convert(self, text: str, target_audience: str) -> str:
        # 허용된 수신 대상 체크
        if target_audience not in PROMPTS:
            raise ValueError(f"지원하지 않는 수신 대상입니다: {target_audience}")
            
        system_instruction = PROMPTS[target_audience]
        
        # 시스템 지침 프롬프트 구성
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_instruction),
            ("human", "{text}")
        ])
        
        # 체인 생성 및 실행
        chain = prompt_template | self.llm
        
        # 비동기 실행 (ainvoke)
        response = await chain.ainvoke({"text": text})
        
        return response.content.strip()
