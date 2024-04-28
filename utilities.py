import streamlit as st
from datetime import datetime

def navigate_to(page_name):
    if 'previous_page' in st.session_state:
        st.session_state['previous_page'].append(st.session_state.page) # add the current page to the stack
    else: st.session_state['previous_page'] = [st.session_state.page]
    st.session_state.page = page_name
    
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
            
# Function to parse datetime strings
def parse_datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')