import json
from models import Person, Event, Entry
from utilities import parse_datetime
import streamlit as st
from datetime import datetime

# Load and parse the JSON files
def load_data():
    with open('./mock-data/people.json', 'r') as file:
        people_data = json.load(file)
        people = [Person(**person) for person in people_data]

    with open('./mock-data/events.json', 'r') as file:
        events_data = json.load(file)
        events = [Event(id=event['id'], date=parse_datetime(event['date']), title=event['title'], summary=event['summary']) for event in events_data]

    with open('./mock-data/entries.json', 'r') as file:
        entries_data = json.load(file)
        entries = [Entry(id=entry['id'], published_date=parse_datetime(entry['published_date']), edited_date=parse_datetime(entry['edited_date']), title=entry['title'], body=entry['body'], people=entry['people'] if 'people' in entry else [], events=entry['events'] if 'events' in entry else []) for entry in entries_data]

    st.session_state.data_loaded = True

    return people, events, entries

def update_data(text, response, people, events, entries):
    # This is a simplified example. You will need to write the logic based on actual response parsing.
    try: 
        extracted_data = json.loads(response)  # Assuming response is JSON formatted
    except:
        # TODO: Add a second pass, giving gpt all the previous info plus the JSON it returned and tell it to iterate on that JSON
        with st.expander("Response"):
            st.markdown(f"```json\n{response}\n```")
        return

    mentioned_people = extracted_data['People']
    mentioned_events = extracted_data['Events']

    # Update people and events
    for person in mentioned_people:
        if "id" not in person or not any(p.id == person['id'] for p in people):
            new_id = max(p.id for p in people) + 1
            person["id"] = new_id
            print("---------")
            print(person)
            print("---------")
            people.append(Person(**person))
    
    for event in mentioned_events:
        if "id" not in event or not any(e.id == event['id'] for e in events):
            new_id = max(e.id for e in events) + 1
            event["id"] = new_id
            events.append(Event(**event))

    # Add entry
    new_entry_id = max(e.id for e in entries) + 1
    entries.append(Entry(id=new_entry_id, published_date=datetime.now(), edited_date=datetime.now(), title="New Entry", body=text, people=[p['id'] for p in mentioned_people], events=[e['id'] for e in mentioned_events]))

    return people, events, entries
