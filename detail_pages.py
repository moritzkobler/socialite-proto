import streamlit as st
from utilities import display_cards
from components import display_person, display_event, display_entry
from models import get_entries_for_person, get_entries_for_event, get_events_for_person, get_people_for_event
import json

def display_person_detail(person):
    if 'previous_page' in st.session_state:
        st.button("Back", on_click=lambda: st.session_state.update(page=st.session_state['previous_page'].pop()))
    
    st.write(f"### {person.first_name} {person.last_name}")
    st.image(person.image_url, width=200)
    st.write(f"**Profession:** {person.profession}")
    st.write(f"**Summary:** {person.summary}")
    
    # Display related entries
    related_entries = get_entries_for_person(person.id, st.session_state.entries)
    st.write("### Entries Mentioning This Person")
    display_cards(related_entries, display_entry, limit=None)

    # Display related events
    related_events = get_events_for_person(person.id, st.session_state.entries, st.session_state.events)
    st.write("### Events Related to This Person")
    display_cards(related_events, display_event, limit=None)

def display_event_detail(event):
    if 'previous_page' in st.session_state:
        st.button("Back", on_click=lambda: st.session_state.update(page=st.session_state['previous_page'].pop()))
    
    st.write(f"**Date:** {event.date.strftime('%B %d, %Y') if event.date else '-'}")
    st.write(f"### {event.title}")
    st.write(f"**Summary:** {event.summary}")
    
    # Display related entries
    related_entries = get_entries_for_event(event.id, st.session_state.entries)
    st.write("### Entries Related to This Event")
    display_cards(related_entries, display_entry, limit=None)

    # Display related people
    related_people = get_people_for_event(event.id, st.session_state.entries, st.session_state.people)
    st.write("### People Related to This Event")
    display_cards(related_people, display_person, limit=None)

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
