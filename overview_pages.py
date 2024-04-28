import streamlit as st
from components import display_person, display_event, display_entry
from utilities import display_cards

def display_people_overview():
    if 'previous_page' in st.session_state and len(st.session_state['previous_page']) > 0:
        st.button("Back", on_click=lambda: st.session_state.update(page=st.session_state['previous_page'].pop()))
    
    st.header('People')
    # search = st.text_input('Search People')
    display_cards(st.session_state.people, display_person, cols=3)

def display_events_overview():
    st.header('Events')
    # search = st.text_input('Search Events')
    display_cards(st.session_state.events, display_event, cols=3)

def display_entries_overview():
    if 'previous_page' in st.session_state and len(st.session_state['previous_page']) > 0:
        st.button("Back", on_click=lambda: st.session_state.update(page=st.session_state['previous_page'].pop()))

    st.header('Entries')
    # search = st.text_input('Search Entries')
    display_cards(st.session_state.entries, display_entry, cols=3)