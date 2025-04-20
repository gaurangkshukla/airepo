#from langchain_core import ChatPromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

## environment variables call
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"

## create chatbot
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please provide response to the user queries"),
        ("user","Question:{question}")
    ]
)

## streamlit framework
st.set_page_config(layout="wide")
st.title("Langchain Demo by Gaurang Shukla")
input_text = st.text_input("Search whatever you want : ")

## LLM Call
llm=Ollama(model="llama2")
output_parser=StrOutputParser()

## Chain
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))