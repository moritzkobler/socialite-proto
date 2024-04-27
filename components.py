# components.py
import streamlit as st
from datetime import datetime

def display_person(person):
    with st.container(border=True):
        st.image(person.image_url, width=100)
        st.write(f"**{person.first_name} {person.last_name}**")
        st.write(f"*{person.profession}*")
        st.write(person.summary)

        if st.button(f"See Details",
                 on_click=navigate_to_person_detail, args=(person,), key=f"person-{person.id}"):
            pass  # The button action is handled by the on_click callback

def navigate_to_person_detail(person):
    if 'previous_page' in st.session_state:
        st.session_state['previous_page'].append(st.session_state.page) # add the current page to the stack
    else: st.session_state['previous_page'] = [st.session_state.page]

    st.session_state['current_person'] = person
    st.session_state.page = 'person_detail'

def display_event(event):
    with st.container(border=True):
        st.write(f"### {event.title}")
        event_date = event.date.strftime("%B %d, %Y") if event.date else "-"
        st.write(f"_Date: {event_date}_")
        st.write(event.summary)
    
        if st.button(f"See Details",
                 on_click=navigate_to_event_detail, args=(event,), key=f"event-{event.id}"):
            pass  # The button action is handled by the on_click callback

        
def navigate_to_event_detail(event):
    if 'previous_page' in st.session_state:
        st.session_state['previous_page'].append(st.session_state.page) # add the current page to the stack
    else: st.session_state['previous_page'] = [st.session_state.page]

    st.session_state['current_event'] = event
    st.session_state.page = 'event_detail'

def display_entry(entry):
    with st.container(border=True):
        st.write(f"### {entry.title}")
        published_date = entry.published_date.strftime("%B %d, %Y")
        edited_date = entry.edited_date.strftime("%B %d, %Y")
        st.write(f"_Published: {published_date} | Edited: {edited_date}_")
        st.write(entry.body)

        if st.button(f"See Details",
                    on_click=navigate_to_entry_detail, args=(entry,), key=f"entry-{entry.id}"):
                pass  # The button action is handled by the on_click callback

def navigate_to_entry_detail(entry):
    if 'previous_page' in st.session_state:
        st.session_state['previous_page'].append(st.session_state.page) # add the current page to the stack
    else: st.session_state['previous_page'] = [st.session_state.page]

    st.session_state['current_entry'] = entry
    st.session_state.page = 'entry_detail'

### UI HELPERS
def display_cards(items, display_function, limit=None, cols=None):
    # Sort items by id in descending order and get the last 'limit' items
    sorted_items = sorted(items, key=lambda x: x.id, reverse=True)[:limit if limit else len(items)]

    # Calculate the number of columns needed (maximum 5 or less if fewer items)
    num_columns = cols if cols else max(1, min(len(sorted_items), 5))
    cols = st.columns(num_columns)  # Create columns dynamically based on actual item count

    # Display items in the columns
    for index, item in enumerate(sorted_items):
        with cols[index % num_columns]:
            display_function(item)