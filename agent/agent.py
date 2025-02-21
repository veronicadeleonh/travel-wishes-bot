import json
from dotenv import load_dotenv
from openai import OpenAI
from agent.tools import TOOLS, search_web
from pydantic import BaseModel, Field


load_dotenv()

class TripSummary(BaseModel):
    summary: str = Field(description="The summary of the trip, including the information in all other keys.")
    destination: str = Field(description="The name of the location.")
    local_timezone: str = Field(description="The local timezone of the location.")
    language: str = Field(description="The main language spoken in the area.")
    currency: str = Field(description="The local currency used.")
    landscape_types: list[str] = Field(description="A list of landscape types (e.g., desert, mountain, forest).")
    best_months_to_visit: list[str] = Field(description="A list of months that are best for visiting.")
    budget: str = Field(description="The typical cost level for a visit (e.g., €€€, €€).")
    visa_requirements: str = Field(description="Visa requirements for the location.")
    food: str = Field(description="Common or local food in the area. Extend the list of food if there are more than 3.")
    health_requirements: str = Field(description="Health requirements for the location.")
    activities: str = Field(description="Notable activities to do in the area.")
    cover_image: str = Field(description="A cover image for the location.")
    

def trip_creator(messages):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,
        response_format=TripSummary,
    )
    return completion.choices[0].message.parsed


def generate_cover_image(prompt):
    client = OpenAI()
    response = client.images.generate(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url # Return the generated image URL


def agent(messages):

    # Initialize the OpenAI client
    client = OpenAI()

    # Make the OpenAI API call to extract the events
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS
    )

    # Parse the response
    response = completion.choices[0].message

    agent_response = {
        "content": "",
        "trip_summary": {}
    }

    # Parse the response to get the tool call arguments
    if response.tool_calls:
        # Process each tool call
        for tool_call in response.tool_calls:
            # Get the tool call arguments
            tool_call_arguments = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "search_web":
                print(f"Searching the web: {tool_call_arguments['query']}")
                search_results = search_web(tool_call_arguments["query"])
                messages.append({"role": "assistant", "content": f"{tool_call_arguments["query"]}: {search_results}"})
        print(f"Creating trip summary: {tool_call_arguments}")
        trip_summary = trip_creator(messages)
        agent_response["trip_summary"] = json.loads(trip_summary.model_dump_json())
    else:
        # If there are no tool calls, return the response content
        agent_response["content"] = response.content
    return agent_response