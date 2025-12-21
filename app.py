import streamlit as st
from utils.data_manager import DataManager
from utils.ui_manager import UIManager
from utils.auth_manager import AuthManager
from views.dashboard import show_dashboard
from views.report import show_report_page
from views.admin import show_admin_page
from views.my_reports import show_my_reports_page
from views.auth import show_login_page, show_register_page

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="NagarNirman", 
    page_icon="favicon.png", 
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar completely
)

# 2. Initialize Data & Auth & Theme
DataManager.init_db()
AuthManager.init_session()
UIManager.init_theme()

# 3. Handle Session Persistence
if not AuthManager.is_authenticated():
    token = st.query_params.get('st_token')
    if token:
        if AuthManager.validate_session(token):
            st.rerun()

UIManager.load_css()

# 3. Render Navbar
current_page = UIManager.render_navbar()

# 4. Route to appropriate page based on navbar selection
if current_page == "home":
    show_dashboard()
elif current_page == "login":
    show_login_page()
elif current_page == "register":
    show_register_page()
elif current_page == "my_reports":
    show_my_reports_page()
elif current_page == "submit_report":
    show_report_page()
elif current_page == "admin":
    show_admin_page()
else:
    show_dashboard()  # Default page
# 5. Render Footer
UIManager.render_footer()
