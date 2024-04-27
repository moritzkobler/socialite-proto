import streamlit as st
from components import display_cards, display_person, display_event
import json

def display_person_detail(person):
    if 'previous_page' in st.session_state:
        st.button("Back", on_click=lambda: st.session_state.update(page=st.session_state['previous_page'].pop()))
    
    st.write(f"### {person.first_name} {person.last_name}")
    st.image(person.image_url, width=200)
    st.write(f"**Profession:** {person.profession}")
    st.write(f"**Summary:** {person.summary}")

def display_event_detail(event):
    if 'previous_page' in st.session_state:
        st.button("Back", on_click=lambda: st.session_state.update(page=st.session_state['previous_page'].pop()))
    
    st.write(f"**Date:** {event.date.strftime('%B %d, %Y')}")
    st.write(f"### {event.title}")
    st.write(f"**Summary:** {event.summary}")

def display_entry_detail(entry):
    if 'previous_page' in st.session_state:
        st.button("Back", on_click=lambda: st.session_state.update(page=st.session_state['previous_page'].pop()))
    
    st.write(f"### {entry.title}")
    st.write(f"**Published Date:** {entry.published_date.strftime('%B %d, %Y')}")
    st.write(f"**Edited Date:** {entry.edited_date.strftime('%B %d, %Y')}")
    st.write(f"**Body:** {entry.body}")

    # Display associated people if there are any
    if entry.people:
        st.write("### People Mentioned")
        mentioned_people = [person for person in st.session_state.people if person.id in entry.people]
        display_cards(mentioned_people, display_person, limit=None)  # No limit on number of cards

    # Display associated events if there are any
    if entry.events:
        st.write("### Events Mentioned")
        mentioned_events = [event for event in st.session_state.events if event.id in entry.events]
        display_cards(mentioned_events, display_event, limit=None)  # No limit on number of cards
