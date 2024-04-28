import streamlit as st
from components import display_person, display_event, display_entry
from utilities import display_cards, navigate_to
import json
from open_ai import query_openai, create_openai_analysis_prompt, create_openai_example_entry_prompt
from data_management import update_data

def generate_entry():
    try:
        prompt = create_openai_example_entry_prompt(st.session_state.people)
        response = query_openai(prompt)
        st.session_state["new_entry"] = response
    except ValueError as e:
        st.session_state["message"] = e
        st.session_state["message_type"] = "error"
    
def analyze_entry(text_area):
    try: 
        prompt = create_openai_analysis_prompt(text_area, st.session_state.people, st.session_state.events)
        response = query_openai(prompt)
        update_data(text_area, response, st.session_state.people, st.session_state.events, st.session_state.entries)
        st.session_state["message"] = "Entry added and data updated!"
        st.session_state["message_type"] = "success"
        st.session_state['analysis_response'] = response
                
    except ValueError as e:
        st.session_state["message"] = e
        st.session_state["message_type"] = "error"
        

def display_home():
    st.header('Add new entry')
    
    
    if "new_entry" not in st.session_state:
        st.session_state["new_entry"] = "Today I met Alice Johnson, Steve Bucelli and their daughters Helga and Hufflepuff at the Charity Ball. We then went on to go to the library where we had a huge party with some crazy things going on."
    
    text_area = st.text_area("Enter the details of the new entry:", key="new_entry")
    if 'message' in st.session_state:
        if st.session_state["message_type"] == "success":
            st.success(st.session_state["message"])
            
            if "debug" in st.session_state and st.session_state.debug:
                with st.expander("Response", expanded=False):
                    st.markdown(f"```json\n{st.session_state.analysis_response}\n```")
                    
        elif st.session_state["message_type"] == "error":
            st.error(st.session_state["message"])
            
        # Clear message after displaying to avoid re-displaying on refresh
        del st.session_state["message"]
        del st.session_state["message_type"]
    
    st.button('Submit', on_click=analyze_entry, args=(text_area,))
    
    if st.session_state.prototype: st.button('Generate Example Entry', on_click=generate_entry)
            
    if "debug" in st.session_state and st.session_state.debug:
        st.header('Debug')
        with st.expander("People", expanded=False):
            st.markdown(f"```json\n{json.dumps([i.to_dict() for i in st.session_state.people], indent=4)}\n```")

        with st.expander("Events", expanded=False):
            st.markdown(f"```json\n{json.dumps([i.to_dict() for i in st.session_state.events], indent=4)}\n```")

        with st.expander("Entries", expanded=False):
            st.markdown(f"```json\n{json.dumps([i.to_dict() for i in st.session_state.entries], indent=4)}\n```")

    st.header('Latest People')
    display_cards(st.session_state.people, display_person, limit=3, cols=3)
    if st.button('See All', on_click=navigate_to, args=("people",), key="see-all-people"): pass
        
    st.header('Latest Events')
    display_cards(st.session_state.events, display_event, limit=3, cols=3)
    if st.button('See All', on_click=navigate_to, args=("events",), key="see-all-events"): pass

    st.header('Latest Entries')
    display_cards(st.session_state.entries, display_entry, limit=3, cols=3)
    if st.button('See All', on_click=navigate_to, args=("entries",), key="see-all-entries"): pass
