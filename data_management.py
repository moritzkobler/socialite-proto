import json
from models import Person, Event, Entry
from utilities import parse_datetime
import streamlit as st
from datetime import datetime
import os
import requests

BACKEND_URL = os.environ.get('BACKEND_URL')
GRAPHQL_ENDPOINT = f"{BACKEND_URL}/graphql"

PEOPLE_QUERY = '''
query {
    allPeople {
        id
        firstName
        lastName
        profession
        summary
        imageUrl
        entries {
            id
            title
            body
            publishedDate
            editedDate
        }
        events {
            id
            date
            title
            summary
        }
    }
}
'''   
EVENTS_QUERY = '''
query {
    allEvents {
        id
        date
        title
        summary
        entries {
            id
            title
            body
            publishedDate
            editedDate
        }
        people {
            id
            firstName
            lastName
            profession
            summary
            imageUrl
        }
    }
}
'''
ENTRIES_QUERY = '''
query {
    allEntries {
        id
        title
        body
        publishedDate
        editedDate
        people {
            id
            firstName
            lastName
            profession
            summary
            imageUrl
        }
        events {
            id
            date
            title
            summary
        }
    }
}
'''

# Load data from the backend
def parse_datetime(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%d')

def fetch_graphql(query, variables=None, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'

    response = requests.post(GRAPHQL_ENDPOINT, json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        if response.status_code == 400: # TODO: need to properly handle this case... to only react if the token is expired rather than a generic 400...
            st.query_params.pop("token")
            st.rerun()
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

def load_data():
    token = st.session_state.token
    people_data = fetch_graphql(PEOPLE_QUERY, token=token)['data']['allPeople']
    events_data = fetch_graphql(EVENTS_QUERY, token=token)['data']['allEvents']
    entries_data = fetch_graphql(ENTRIES_QUERY, token=token)['data']['allEntries']

    people = [Person(
            id=person['id'],
            first_name=person['firstName'],
            last_name=person['lastName'],
            profession=person['profession'],
            summary=person['summary'],
            image_url=person['imageUrl'],
            events=[Event(
                id=event['id'], 
                date=parse_datetime(event['date']), 
                title=event['title'], summary=event['summary']
            ) for event in person['events']] if 'events' in person else [],
            entries=[Entry(
                id=entry['id'],
                published_date=parse_datetime(entry['publishedDate']),
                edited_date=parse_datetime(entry['editedDate']),
                title=entry['title'],
                body=entry['body']
            ) for entry in person['entries']] if 'entries' in person else []
        ) for person in people_data]
    
    events = [Event(
                id=event['id'], 
                date=parse_datetime(event['date']), 
                title=event['title'], 
                summary=event['summary'],
                people=[Person(
                    id=person['id'], 
                    first_name=person['firstName'], 
                    last_name=person['lastName'], 
                    profession=person['profession'], 
                    summary=person['summary'], 
                    image_url=person['imageUrl']
                ) for person in event['people']] if 'people' in event else [],
                entries=[Entry(
                    id=entry['id'],
                    published_date=parse_datetime(entry['publishedDate']),
                    edited_date=parse_datetime(entry['editedDate']),
                    title=entry['title'],
                    body=entry['body']
                ) for entry in event['entries']] if 'entries' in event else []
            ) for event in events_data]
    
    entries = [Entry(
            id=entry['id'], 
            published_date=parse_datetime(entry['publishedDate']), 
            edited_date=parse_datetime(entry['editedDate']), 
            title=entry['title'], 
            body=entry['body'], 
            people=[Person(
                id=person['id'], 
                first_name=person['firstName'], 
                last_name=person['lastName'], 
                profession=person['profession'], 
                summary=person['summary'], 
                image_url=person['imageUrl']
            ) for person in entry['people']] if 'people' in entry else [], 
            events=[Event(
                id=event['id'], 
                date=parse_datetime(event['date']), 
                title=event['title'], 
                summary=event['summary']
            ) for event in entry['events']] if 'events' in entry else []
        ) for entry in entries_data
    ]

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
