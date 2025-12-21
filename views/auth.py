import streamlit as st
from utils.auth_manager import AuthManager

def show_login_page():
    """Display the login form."""
    st.title("🔐 Login")
    st.markdown("Welcome back! Please login to continue.")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 1])
        submitted = col1.form_submit_button("🔓 Login", use_container_width=True)
        
        if submitted:
            success, message = AuthManager.login(username, password)
            if success:
                st.success(message)
                # Redirect based on role
                if AuthManager.is_admin():
                    st.session_state.current_page = "admin"
                else:
                    st.session_state.current_page = "home"
                st.rerun()
            else:
                st.error(message)
    
    st.markdown("---")
    st.markdown("Don't have an account? Go to **Register** from the sidebar.")


def show_register_page():
    """Display the registration form."""
    st.title("📝 Create Account")
    st.markdown("Join NagarNirman to report and track infrastructure issues in your city.")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        full_name = col1.text_input("Full Name", placeholder="Enter your full name")
        email = col2.text_input("Email", placeholder="Enter your email address")
        
        username = st.text_input("Username", placeholder="Choose a unique username (min 3 characters)")
        
        col_pass1, col_pass2 = st.columns(2)
        password = col_pass1.text_input("Password", type="password", placeholder="Min 6 characters")
        confirm_password = col_pass2.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        submitted = st.form_submit_button("📋 Register", use_container_width=True)
        
        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = AuthManager.register_user(username, password, email, full_name)
                if success:
                    st.success(message)
                    st.info("You can now login with your credentials.")
                else:
                    st.error(message)
    
    st.markdown("---")
    st.markdown("Already have an account? Go to **Login** from the sidebar.")


def show_logout_button():
    """Display logout button in sidebar."""
    user = AuthManager.get_current_user()
    role = AuthManager.get_role()
    
    if user:
        role_badge = "👑 Admin" if role == "admin" else "👤 User"
        st.sidebar.markdown(f"**{role_badge}**: {user.get('full_name', user.get('username', 'User'))}")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        AuthManager.logout()
        st.rerun()
