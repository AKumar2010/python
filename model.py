
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv

class LlmModel:


    def get_llm(self):
        """Loads OpenAi model"""
        load_dotenv()
        llm=ChatOpenAI(model='gpt-5.4-mini',temperature=0.3)
        return llm


    