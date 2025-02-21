import os
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient
import json
load_dotenv()


# Define the tools
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search the web for information"
                }
            },
            "required": [
                "query"
            ],
                "additionalProperties": False
            },
            "strict": True
        },
    },
]


# Function to search the web
def search_web(query):
    # Initialize Tavily
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return "\n".join(f"{{Content: {result['content']} \n URL: {result['url']}}}" for result in tavily.search(query, search_depth="basic")["results"])


