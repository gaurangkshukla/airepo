import os

from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()
#TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
#os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

tool = TavilySearchResults()
print(tool.invoke({"query": "who is Mahatma Gandhi"}))