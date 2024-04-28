import json
from openai import OpenAI
import os
import streamlit as st

def create_openai_analysis_prompt(text, people, events):
    people_json = json.dumps([person.to_dict() for person in people], indent=4)
    events_json = json.dumps([event.to_dict() for event in events], indent=4)
    
    prompt = f"""
    System Prompt: Given the text entry below, identify all mentioned people and events in that text. Reuse existing IDs from the provided lists if matches are found.
    Make sure to also identify new people and events mentioned in the text if you can't match them with any of the existing ones.
    If they are new people or events that don't match any of the existing ones, don't assign them any id.
    An event can be anything from catching up for coffee to going to the cinema to a charity gala.
    
    ---
    Text: {text}
    Existing People: {people_json}
    Existing Events: {events_json}
    ---
    Identify and list any people and events mentioned in the text in the following format, making sure it is a valid JSON with entries for "People" and "Events":
    Make absolutely sure the structure returned looks like this: {{ "People": [ list of people ], "Events": [ list of events ]}}

    If you can't find a value for a field, don't sent that field.
    If there are no people or events identified, still send an empty array.
    """
    
    return prompt

def create_openai_example_entry_prompt(people):
    people_json = json.dumps([person.to_dict() for person in people], indent=4)
    
    prompt = f"""
    System Prompt: Write a short for a journal-type entry of 50 words or shorter that mentions up to 3 people.
    They entry and the people met should be tied to one or more specific events, like a gallery opening, a charity ball, a coffee date or similar. 
    People shuld be a mix of existing people from the json mentioned below and new people you should come up with.
    If you choose to add new people mention their first and last names. For existing people you can just use their first names.
    Make the journal either very dark and serious and somber, or very lighthearted, quirky, and fun.
    
    ---
    Existing People: {people_json}
    
    Only return the journal entry itself without any headings or other information.
    ---
    """
    
    return prompt    

def query_openai(prompt, model_override=None):
    if ("api_key" not in st.session_state or st.session_state.api_key == "") and not os.getenv('OAI_SOCIALITE_API_KEY'): raise ValueError("Enter an API key in the menu to the left!")

    print(st.session_state.api_key)

    client = OpenAI(
        api_key = st.session_state.api_key if "api_key" in st.session_state and st.session_state.api_key != "" else os.getenv('OAI_SOCIALITE_API_KEY')
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model = model_override if model_override else (st.session_state.model if "model" in st.session_state and st.session_state.model else "gpt-4"),
        )
    except Exception as e:
        raise ValueError("There was an issue with the request. Make sure the API key you entered is correct...")
        return
        

    return response.choices[0].message.content.strip()
