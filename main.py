
from utils.utility import load_apiKey
from agent.agent import load_dotenv, llm
from agent.rag import create_embedding
from langchain.agents import create_agent
from model import doc
from agent.rag import RagStuff


def execute():
   RagStuff().tryRag()
    


execute()