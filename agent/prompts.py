from datetime import datetime


def get_system_prompt():

    return f"""
    - You are a helpful travel assistant with web search capabilities. 
    - Use the search_web function to search the web for information and that requires real-time data.

    CURRENT DATE AND TIME:
    {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    """