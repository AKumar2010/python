
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv

class llmModel:
    def get_llm():
        load_dotenv()
        llm=ChatOpenAI(model='gpt-5.4-mini',temperature=0.3)
        return llm


    