import streamlit as st
from utilities import navigate_to
from detail_pages import display_person_detail, display_entry_detail, display_event_detail
from overview_pages import display_people_overview, display_events_overview, display_entries_overview
from home_page import display_home
from data_management import load_data
import requests
import extra_streamlit_components as stx # https://github.com/Mohamed-512/Extra-Streamlit-Components/blob/master/README.md
import time
import os

backend_url = os.environ.get('BACKEND_URL')

# Cookie handling beyond refresh
@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

# Login & registration
def login_registration():
    choice = st.sidebar.radio("Welcome! You're currently logged out!", ("Login", "Register", "Forgot Password"))
    
    if choice == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"): login(email, password)
            
    elif choice == "Register":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        
        if st.button("Register"):
            response = requests.post(f"{backend_url}/auth/register", json={"email": email, "password": password, "first_name": first_name, "last_name": last_name})
            
            if response.status_code == 201:
                st.success("Registration successful! Logging you in...")
                login(email, password, 5)
                
            else:
                st.error("Registration failed")
    elif choice == "Forgot Password":
        st.header("Forgot Password")
        email = st.text_input("Email")
        
        if st.button("Reset Password"):
            response = requests.post(f"{backend_url}/auth/request-password-reset", json={"email": email})
            
            if response.status_code == 200:
                st.success("Password reset email sent!")
            else:
                st.error("Password reset failed")

def login(email, password, wait_time=0):
    response = requests.post(f"{backend_url}/auth/login", json={"email": email, "password": password})
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        st.session_state['token'] = token
        cookie_manager.set('token', token)
        time.sleep(wait_time)
        st.rerun()
    else:
        st.error("Login failed")
    
def password_reset(token):
    st.header("Reset Password")
    password = st.text_input("New Password", type="password")
    
    if st.button("Reset"):
        response = requests.post(f"{backend_url}/auth/reset-password/{token}", json={"new_password": password})
        
        if response.status_code == 200:
            st.success("Password reset successful! Logging you in...")
            st.query_params.pop("pwtoken")
            login(response.json().get("email"), password, 5)
        elif response.status_code == 400:
            st.error("Invalid or expired link. Please try resetting the password again to receive a new email.")
        
# App content
def protected_route():    
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
        
    st.sidebar.checkbox("Debug Mode", value=False, key='debug')
    st.sidebar.checkbox("Prototype Features", value=False, key='prototype')
    
    # logout button
    if st.sidebar.button("Logout"):
        del st.session_state['token']
        cookie_manager.delete('token')
        st.session_state.clear()
        st.rerun()

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
    
def main():
    # TODO: use proper parameter routing to do all this...
    if "pwtoken" in st.query_params:
        password_reset(st.query_params.pwtoken)
        return
    
    if not 'token' in st.session_state:
        token = cookie_manager.get('token')  # Try to get token from cookies
        if token:
            st.session_state['token'] = token
        
    if 'token' in st.session_state:
        protected_route()
    else:
        login_registration()
    
if __name__ == "__main__":
    st.set_page_config(layout="wide")  # Options are "wide" or "centered"
    cookie_manager = get_manager()
    
    main()