import os
from tavily import TavilyClient
from dotenv import load_dotenv
import gradio as gr

load_dotenv()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#Python Progam by Gaurang Shukla

def search_with_tavily(query):
    try:
        response = tavily_client.search(query)
        # Format the results
        results = []
        if 'results' in response:
            for i, result in enumerate(response['results'], 1):
                #results.append(f"{i}. {result['title']}\n   URL: {result['url']}\n   Content: {result['content'][:200]}...")
                results.append(f"{i}. {result['title']}\n   Content: {result['content'][:200]}...")
            
            return "\n\n".join(results)
        else:
            return "No results found or there was an error with the API."

    except Exception as e:
        return f"An error occurred: {str(e)}"

#print(search_with_tavily("who is Sardar Patel"))

title = "✨ Tavily Search by Gaurang Shukla ✨"
desc = "🎨 If this inspires you, let others know!"
long_desc = "🌟 Enjoyed this? spread the word! "
# Create Gradio Interface

gr.Interface(search_with_tavily,"text","text", theme=gr.themes.Glass(),
              title=title, description=desc, article=long_desc).launch(share=True)