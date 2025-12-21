import streamlit as st
from utils.auth_manager import AuthManager

def show_login_page():
    """Display the login form with Boss Level UI."""
    st.markdown('<div class="fade-in auth-container">', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <h1 style="text-align:center; margin-bottom:0;">🔐 Login</h1>
            <p style="text-align:center; opacity:0.7; margin-bottom:2rem;">Welcome back to NagarNirman</p>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Username")
        password = st.text_input("Password", type="password", placeholder="Password")
        
        st.markdown('<div style="margin-top:1rem;">', unsafe_allow_html=True)
        submitted = st.form_submit_button("🔓 Unlock Dashboard", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
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
    
    st.markdown('</div>', unsafe_allow_html=True) # End glass-card
    
    if st.button("New here? Create an Account", use_container_width=True):
        st.session_state.current_page = "register"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True) # End auth-container


def show_register_page():
    """Display the registration form with Boss Level UI."""
    st.markdown('<div class="fade-in auth-container" style="max-width:600px;">', unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card">
            <h1 style="text-align:center; margin-bottom:0;">📝 Join Us</h1>
            <p style="text-align:center; opacity:0.7; margin-bottom:2rem;">Start making your city better today</p>
    """, unsafe_allow_html=True)
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        full_name = col1.text_input("Full Name", placeholder="e.g. John Doe")
        email = col2.text_input("Email", placeholder="e.g. john@example.com")
        
        username = st.text_input("Unique Username", placeholder="min 3 characters")
        
        col_pass1, col_pass2 = st.columns(2)
        password = col_pass1.text_input("Password", type="password", placeholder="min 6 characters")
        confirm_password = col_pass2.text_input("Verify Password", type="password", placeholder="re-enter password")
        
        st.markdown('<div style="margin-top:1rem;">', unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Create Account", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
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
    
    st.markdown('</div>', unsafe_allow_html=True) # End glass-card
    
    if st.button("Already have an account? Login", use_container_width=True):
        st.session_state.current_page = "login"
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True) # End auth-container


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
