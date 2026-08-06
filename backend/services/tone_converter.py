import os
from dotenv import load_dotenv
from langchain_upstage import ChatUpstage
from langchain_core.prompts import PromptTemplate
from backend.prompts.templates import PROMPTS

# Load environmental variables (.env)
load_dotenv()

class ToneConverter:
    def __init__(self):
        # Initialize ChatUpstage with solar-pro3 model (as per current target settings)
        self.llm = ChatUpstage(model="solar-pro3")

    def convert(self, text: str, target_audience: str) -> str:
        # Check if the target audience is supported
        if target_audience not in PROMPTS:
            raise ValueError(f"지원하지 않는 수신 대상입니다: {target_audience}")

        # Fetch prompt template
        prompt_string = PROMPTS[target_audience]
        
        # Build PromptTemplate and format
        prompt_template = PromptTemplate.from_template(prompt_string)
        formatted_prompt = prompt_template.format(text=text)

        # Call Solar-Pro3 model
        response = self.llm.invoke(formatted_prompt)
        
        # Clean response and strip surrounding whitespaces
        return response.content.strip()
