import os
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

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
                    "query": {"type": "string"}
                },
                "required": ["query"]
            },
        },
    },
]


# Function to search the web
def search_web(query):
    # Initialize Tavily
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return "\n".join(result["content"] for result in tavily.search(query, search_depth="basic")["results"])


# Function to invoke the model
def invoke_model(messages):
    # Initialize the OpenAI client
    client = OpenAI()

    # Make a ChatGPT API call with tool calling
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return completion.choices[0].message.content


# Function to get the embeddings of a string
def get_embeddings(string_to_embed):
    client = OpenAI()  
    response = client.embeddings.create(
        input=string_to_embed,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding