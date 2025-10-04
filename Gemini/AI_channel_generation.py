import streamlit as st
from google import genai
from google.genai import types
import ast

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Initializing the Google search tool connection with gemini api
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Configure generation settings
config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=list[str]
)

# Configure google tool compatible settings
config2 = types.GenerateContentConfig(
    temperature=0,
    tools=[grounding_tool]
)


def ia_channel_request(prompt: str) -> list[str]:
    print("Generating request...")
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt, config=config)
    if isinstance(response.parsed, list):
        channels: list[str] = response.parsed
    else:
        channels = []
        print("Gemini did not send a list")
    return channels


def ia_google_search_request(prompt: str) -> list[str]:
    print("Generating request...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config2,
    )
    response_list_text = response.text
    # Check if the answer of gemini is truly a list
    try:
        response_list = ast.literal_eval(response_list_text)
        if isinstance(response_list, list):
            return response_list
        else:
            return []
    except (ValueError, SyntaxError):
        # If is not a list the tool inform the user
        st.write(f"IA MESSAGE: {response_list_text}")
        st.error(f"GEMINI DIDN'T SEND A LIST")
        return []
