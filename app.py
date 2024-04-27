import streamlit as st
from models import Person, Event, Entry
import json
from datetime import datetime
from components import display_person, display_event, display_entry, display_cards
from detail_pages import display_person_detail, display_entry_detail
from openai import OpenAI
client = OpenAI(
    api_key = "sk-proj-b13Bh4Zx5UEh8DhZdNcuT3BlbkFJFj6FRXSc854kEq2v346f" # ONLY FOR DEVELOPMENT, NOT IN PRODUCTION
)

# Function to parse datetime strings
def parse_datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

### DATA MANAGEMENT
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
        print(response)
        extracted_data = json.loads(response)  # Assuming response is JSON formatted
    except:
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

### OPENAI
def create_openai_prompt(text, people, events):
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
    It should look like this: {{ "People": [ list of people ], "Events": [ list of events ]}}

    If you can't find a value for a field, don't sent that field.
    If there are no people or events identified, still send an empty array.
    """
    return prompt

def query_openai(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )

    return response.choices[0].message.content.strip()

### CONTENT
# Call the function to load data
if 'data_loaded' not in st.session_state:
    st.session_state.people, st.session_state.events, st.session_state.entries = load_data()

# Placeholder for the logo, replace 'logo.png' with the path to your actual logo file
LOGO_IMAGE = './assets/img/logo.png'

# Initialize session state keys if they don't exist
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Helper function to handle page navigation
def navigate_to(page_name):
    st.session_state.page = page_name

# Top bar with logo, app name, and New Entry button
st.sidebar.image(LOGO_IMAGE, width=100)
st.sidebar.title('Socialite')
if st.sidebar.button('New Entry'):
    navigate_to('home')

# Sidebar navigation
st.sidebar.header('Navigation')
nav_items = ['Home', 'Entries', 'People', 'Events']
for item in nav_items:
    if st.sidebar.button(item):
        navigate_to(item.lower())

# Page routing
if st.session_state.page == 'home':
    st.header('Add new entry')
    text_area = st.text_area("Enter the details of the new entry:", value="Today I met Alice Johnson and Steve Bucelli at the Charity Ball, which was so nice...")
    if st.button('Submit'):
        prompt = create_openai_prompt(text_area, st.session_state.people, st.session_state.events)
        response = query_openai(prompt)
        update_data(text_area, response, st.session_state.people, st.session_state.events, st.session_state.entries)
        st.success('Entry added and data updated!')
        with st.expander("Response", expanded=False):
            st.markdown(f"```json\n{response}\n```")

    with st.expander("People", expanded=False):
        st.markdown(f"```json\n{json.dumps([i.to_dict() for i in st.session_state.people], indent=4)}\n```")

    with st.expander("Events", expanded=False):
        st.markdown(f"```json\n{json.dumps([i.to_dict() for i in st.session_state.events], indent=4)}\n```")

    with st.expander("Entries", expanded=False):
        st.markdown(f"```json\n{json.dumps([i.to_dict() for i in st.session_state.entries], indent=4)}\n```")

    st.header('Latest People')
    display_cards(st.session_state.people, display_person, limit=5)

    st.header('Latest Events')
    display_cards(st.session_state.events, display_event, limit=5)

    st.header('Latest Entries')
    display_cards(st.session_state.entries, display_entry, limit=5)

### Overview Pages
elif st.session_state.page == 'entries':
    st.header('Entries')
    search = st.text_input('Search Entries')
    st.write('Grid of entries would go here. Clicking on an entry would redirect to its details.')

elif st.session_state.page == 'people':
    st.header('People')
    search = st.text_input('Search People')
    st.write('Grid of people would go here. Clicking on a person would redirect to their details.')

elif st.session_state.page == 'events':
    st.header('Events')
    search = st.text_input('Search Events')
    st.write('Grid of events would go here. Clicking on an event would redirect to its details.')

### Detail Pages
elif st.session_state.page == 'person_detail':
    display_person_detail(st.session_state['current_person'])

elif st.session_state.page == 'event_detail':
    display_event_detail(st.session_state['current_event'])

elif st.session_state.page == 'entry_detail':
    display_entry_detail(st.session_state['current_entry'])