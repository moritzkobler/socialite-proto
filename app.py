import streamlit as st
from utilities import display_cards, navigate_to
from components import display_person, display_event, display_entry
from detail_pages import display_person_detail, display_entry_detail, display_event_detail
from overview_pages import display_people_overview, display_events_overview, display_entries_overview
from home_page import display_home
from data_management import load_data

### CONTENT
# Call the function to load data
if 'data_loaded' not in st.session_state:
    st.session_state.people, st.session_state.events, st.session_state.entries = load_data()

# Placeholder for the logo, replace 'logo.png' with the path to your actual logo file
LOGO_IMAGE = './assets/img/logo.png'

# Initialize session state keys if they don't exist
if 'page' not in st.session_state:
    st.session_state.page = 'home'

### ACTUAL PAGE
st.set_page_config(layout="wide")  # Options are "wide" or "centered"

# Top bar with logo, app name, and New Entry button
# st.sidebar.image(LOGO_IMAGE, width=100)
st.sidebar.title('Socialite')

### SIDEBAR
# Sidebar navigation
st.sidebar.header('Navigation')
nav_items = ['Home', 'Entries', 'People', 'Events']
for item in nav_items:
    if st.sidebar.button(item):
        navigate_to(item.lower())

# Input for API key & model
api_key = st.sidebar.text_input("Enter OpenAI API Key:")
if api_key:
    st.session_state.api_key = api_key  # Store API key in session state
    st.sidebar.success("API key is set!")
    
# Input for API key & model
magic_word = st.sidebar.text_input("... or the magic words:")
if magic_word:
    if magic_word == st.secrets["MAGIC_WORD"]:
        st.session_state.api_key = st.secrets["OAI_SOCIALITE_API_KEY"]  # Store API key in session state
        st.sidebar.success("API key is set!")
    else:
        st.sidebar.error("Begone, thief! Those aren't the magic words I'm after!")

selected_model = st.sidebar.selectbox("Select Model to Use", ["gpt-4o", "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"])
if selected_model:
    st.session_state.model = selected_model
    
debug_mode = st.sidebar.checkbox("Debug Mode", value=False, key='debug')
debug_mode = st.sidebar.checkbox("Prototype Features", value=False, key='prototype')

### ROUTING
### HOME
if st.session_state.page == 'home': display_home()
    
### Overview Pages
elif st.session_state.page == 'people': display_people_overview()
elif st.session_state.page == 'events': display_events_overview()
elif st.session_state.page == 'entries': display_entries_overview()

### Detail Pages
elif st.session_state.page == 'person_detail': display_person_detail(st.session_state['current_person'])
elif st.session_state.page == 'event_detail': display_event_detail(st.session_state['current_event'])
elif st.session_state.page == 'entry_detail': display_entry_detail(st.session_state['current_entry'])