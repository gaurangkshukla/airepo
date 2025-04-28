import os
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import gradio as gr

#Python Progam by Gaurang Shukla

load_dotenv()
tavily_client = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))


def format_results(response): 
    results = []
    if len(response)>0:
        for idx, result in enumerate(response): 
            results.append(f"{idx + 1}: {result['title']} \n {result['content'][:200]}...")
        return "\n\n".join(results)
    else:
        return "No results found or there was an error with the API."

def search_with_tavily(query):
    try:
        response = tavily_client.invoke(query)
        return format_results(response)

    except Exception as e:
        return f"An error occurred: {str(e)}"

#print(search_with_tavily("who is Sardar Patel"))

title = "✨ Tavily Search Langchain by Gaurang Shukla ✨"
desc = "🎨 If this inspires you, let others know!"
long_desc = "🌟 Enjoyed this? spread the word! "
# Create Gradio Interface

gr.Interface(search_with_tavily,"text","text", theme=gr.themes.Glass(),
              title=title, description=desc, article=long_desc).launch(share=True)