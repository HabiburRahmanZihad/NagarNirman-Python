"""
Authentication Manager for NagarNirman
Handles user registration, login, logout, and role-based access control.
"""

import streamlit as st
import json
import os
import hashlib
from datetime import datetime

class AuthManager:
    USERS_FILE = "users_db.json"
    SESSIONS_FILE = "sessions_db.json"
    
    # Admin credentials (hardcoded)
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD_HASH = hashlib.sha256("Pa$$w0rd!".encode()).hexdigest()
    
    @staticmethod
    def _hash_password(password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def _load_users():
        """Load users from JSON file."""
        if os.path.exists(AuthManager.USERS_FILE):
            try:
                with open(AuthManager.USERS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    @staticmethod
    def _save_users(users):
        """Save users to JSON file."""
        try:
            with open(AuthManager.USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
        except IOError as e:
            st.error(f"Failed to save user data: {e}")
    
    @staticmethod
    def _load_sessions():
        """Load sessions from JSON file."""
        if os.path.exists(AuthManager.SESSIONS_FILE):
            try:
                with open(AuthManager.SESSIONS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    @staticmethod
    def _save_sessions(sessions):
        """Save sessions to JSON file."""
        try:
            with open(AuthManager.SESSIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(sessions, f, indent=2, ensure_ascii=False)
        except IOError as e:
            st.error(f"Failed to save session data: {e}")
    
    @staticmethod
    def init_session():
        """Initialize authentication session state."""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'role' not in st.session_state:
            st.session_state.role = None
    
    @staticmethod
    def register_user(username, password, email, full_name):
        """
        Register a new user.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not username or not password or not email:
            return False, "All fields are required."
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters."
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters."
        
        # Check if username is reserved
        if username.lower() == "admin":
            return False, "This username is reserved."
        
        users = AuthManager._load_users()
        
        # Check if username already exists
        if username in users:
            return False, "Username already exists."
        
        # Check if email already exists
        for user_data in users.values():
            if user_data.get('email', '').lower() == email.lower():
                return False, "Email already registered."
        
        # Create new user
        users[username] = {
            "password_hash": AuthManager._hash_password(password),
            "email": email,
            "full_name": full_name,
            "role": "user",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        AuthManager._save_users(users)
        return True, "Registration successful! Please login."
    
    @staticmethod
    def login(username, password):
        """
        Authenticate a user.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password are required."
        
        # Check for admin login
        if username == AuthManager.ADMIN_USERNAME:
            if AuthManager._hash_password(password) == AuthManager.ADMIN_PASSWORD_HASH:
                st.session_state.authenticated = True
                st.session_state.user = {"username": "admin", "full_name": "Administrator"}
                st.session_state.role = "admin"
                return True, "Welcome, Administrator!"
            else:
                return False, "Invalid credentials."
        
        # Check for regular user login
        users = AuthManager._load_users()
        
        if username not in users:
            return False, "Invalid username or password."
        
        user_data = users[username]
        
        if user_data["password_hash"] != AuthManager._hash_password(password):
            return False, "Invalid username or password."
        
        # Login successful
        st.session_state.authenticated = True
        st.session_state.user = {
            "username": username,
            "full_name": user_data.get("full_name", username),
            "email": user_data.get("email", "")
        }
        st.session_state.role = user_data.get("role", "user")
        
        # Create persistent session
        token = AuthManager.create_session(username)
        st.session_state.session_token = token
        
        return True, f"Welcome, {user_data.get('full_name', username)}!"

    @staticmethod
    def create_session(username):
        """Create a new session token for the user."""
        import secrets
        token = secrets.token_urlsafe(32)
        sessions = AuthManager._load_sessions()
        sessions[token] = {
            "username": username,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        AuthManager._save_sessions(sessions)
        return token

    @staticmethod
    def validate_session(token):
        """Validate a session token and log in the user if valid."""
        if not token:
            return False
            
        sessions = AuthManager._load_sessions()
        if token not in sessions:
            return False
            
        session_data = sessions[token]
        username = session_data["username"]
        
        # Admin check
        if username == AuthManager.ADMIN_USERNAME:
            st.session_state.authenticated = True
            st.session_state.user = {"username": "admin", "full_name": "Administrator"}
            st.session_state.role = "admin"
            st.session_state.session_token = token
            st.session_state.current_page = "admin"
            return True
            
        # User check
        users = AuthManager._load_users()
        if username not in users:
            return False
            
        user_data = users[username]
        st.session_state.authenticated = True
        st.session_state.user = {
            "username": username,
            "full_name": user_data.get("full_name", username),
            "email": user_data.get("email", "")
        }
        st.session_state.role = user_data.get("role", "user")
        st.session_state.session_token = token
        st.session_state.current_page = "home"
        return True
    
    @staticmethod
    def logout():
        """Logout the current user."""
        token = st.session_state.get('session_token')
        if token:
            sessions = AuthManager._load_sessions()
            if token in sessions:
                del sessions[token]
                AuthManager._save_sessions(sessions)
        
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.session_token = None
    
    @staticmethod
    def is_authenticated():
        """Check if a user is currently logged in."""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def get_current_user():
        """Get the current logged-in user info."""
        return st.session_state.get('user', None)
    
    @staticmethod
    def get_role():
        """Get the current user's role."""
        return st.session_state.get('role', None)
    
    @staticmethod
    def is_admin():
        """Check if the current user is an admin."""
        return st.session_state.get('role', None) == "admin"
    
    @staticmethod
    def is_user():
        """Check if the current user is a regular user."""
        return st.session_state.get('role', None) == "user"
