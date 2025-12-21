import streamlit as st
import os

class UIManager:
    @staticmethod
    def init_theme():
        """Initialize theme in session state."""
        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'  # Default to dark theme
    
    @staticmethod
    def toggle_theme():
        """Toggle between light and dark theme."""
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
    
    @staticmethod
    def get_theme():
        """Get current theme."""
        return st.session_state.get('theme', 'dark')
    
    @staticmethod
    def load_css(file_path="assets/style.css"):
        """Loads custom CSS from a file based on current theme."""
        theme = UIManager.get_theme()
        
        # Load base CSS
        if os.path.exists(file_path):
            with open(file_path) as f:
                base_css = f.read()
        else:
            base_css = ""
        
        # Navbar CSS
        navbar_css = """
        /* Navbar Styling */
        .navbar {
            background: rgba(22, 27, 34, 0.95);
            backdrop-filter: blur(10px);
            padding: 10px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }
        
        .navbar-logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .navbar-logo img {
            height: 50px;
            width: 50px;
            border-radius: 8px;
        }
        
        .navbar-brand {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(45deg, #FF4B4B, #FF914D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .navbar-menu {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .navbar-right {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .nav-button {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 8px 16px;
            border-radius: 6px;
            color: #E0E0E0;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }
        
        .nav-button:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: #FF4B4B;
            transform: translateY(-2px);
        }
        
        .nav-button-active {
            background: linear-gradient(90deg, #FF4B4B 0%, #FF914D 100%);
            border-color: #FF4B4B;
            color: white;
        }
        
        .user-badge {
            background: rgba(102, 126, 234, 0.2);
            border: 1px solid rgba(102, 126, 234, 0.4);
            padding: 6px 12px;
            border-radius: 20px;
            color: #E0E0E0;
            font-size: 14px;
        }
        
        /* Hide sidebar toggle */
        [data-testid="collapsedControl"] {
            display: none;
        }
        """
        
        # Theme-specific CSS
        if theme == 'light':
            theme_css = """
            /* Light Theme Overrides */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
            }
            
            .navbar {
                background: rgba(255, 255, 255, 0.95) !important;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            
            .nav-button {
                background: rgba(0, 0, 0, 0.05) !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
                color: #1a1a1a !important;
            }
            
            .nav-button:hover {
                background: rgba(0, 0, 0, 0.1) !important;
            }
            
            .user-badge {
                background: rgba(102, 126, 234, 0.15) !important;
                border: 1px solid rgba(102, 126, 234, 0.3) !important;
                color: #1a1a1a !important;
            }
            
            h1, h2, h3, h4, h5, h6, p, span, div, label {
                color: #1a1a1a !important;
            }
            
            .stMarkdown {
                color: #1a1a1a !important;
            }
            
            .report-card {
                background: rgba(255, 255, 255, 0.9) !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
                color: #1a1a1a !important;
            }
            
            .report-card h4, .report-card p {
                color: #1a1a1a !important;
            }
            
            /* Input fields */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {
                background-color: rgba(255, 255, 255, 0.9) !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.2) !important;
            }
            
            /* Buttons */
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
            }
            
            /* Metrics */
            [data-testid="stMetricValue"] {
                color: #1a1a1a !important;
            }
            """
        else:
            theme_css = ""
        
        # Apply combined CSS
        st.markdown(f'<style>{base_css}\n{navbar_css}\n{theme_css}</style>', unsafe_allow_html=True)
    
    @staticmethod
    def render_navbar():
        """Render horizontal navbar and return selected page."""
        from utils.auth_manager import AuthManager
        
        # Initialize current page in session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        
        # Create navbar container
        navbar_html = '<div class="navbar">'
        
        # Logo and brand
        logo_path = "logo/logo.png"
        if os.path.exists(logo_path):
            navbar_html += f'<div class="navbar-logo"><img src="data:image/png;base64,{UIManager._get_image_base64(logo_path)}"><span class="navbar-brand">NagarNirman</span></div>'
        else:
            navbar_html += '<div class="navbar-logo"><span class="navbar-brand">🏗️ NagarNirman</span></div>'
        
        navbar_html += '</div>'
        st.markdown(navbar_html, unsafe_allow_html=True)
        
        # Navigation buttons
        col_logo, col_menu, col_right = st.columns([2, 6, 3])
        
        with col_menu:
            if not AuthManager.is_authenticated():
                # Guest menu
                cols = st.columns(3)
                if cols[0].button("🌆 Home & Map", use_container_width=True, type="primary" if st.session_state.current_page == "home" else "secondary"):
                    st.session_state.current_page = "home"
                    st.rerun()
                if cols[1].button("🔐 Login", use_container_width=True, type="primary" if st.session_state.current_page == "login" else "secondary"):
                    st.session_state.current_page = "login"
                    st.rerun()
                if cols[2].button("📝 Register", use_container_width=True, type="primary" if st.session_state.current_page == "register" else "secondary"):
                    st.session_state.current_page = "register"
                    st.rerun()
            
            elif AuthManager.is_admin():
                # Admin menu
                cols = st.columns(2)
                if cols[0].button("🌆 Home & Map", use_container_width=True, type="primary" if st.session_state.current_page == "home" else "secondary"):
                    st.session_state.current_page = "home"
                    st.rerun()
                if cols[1].button("👮 Admin Dashboard", use_container_width=True, type="primary" if st.session_state.current_page == "admin" else "secondary"):
                    st.session_state.current_page = "admin"
                    st.rerun()
            
            else:
                # User menu
                cols = st.columns(3)
                if cols[0].button("🌆 Home & Map", use_container_width=True, type="primary" if st.session_state.current_page == "home" else "secondary"):
                    st.session_state.current_page = "home"
                    st.rerun()
                if cols[1].button("📋 My Reports", use_container_width=True, type="primary" if st.session_state.current_page == "my_reports" else "secondary"):
                    st.session_state.current_page = "my_reports"
                    st.rerun()
                if cols[2].button("📢 Submit Report", use_container_width=True, type="primary" if st.session_state.current_page == "submit_report" else "secondary"):
                    st.session_state.current_page = "submit_report"
                    st.rerun()
        
        with col_right:
            right_cols = st.columns([2, 1] if AuthManager.is_authenticated() else [1])
            
            if AuthManager.is_authenticated():
                # User badge
                user = AuthManager.get_current_user()
                role_badge = "👑 Admin" if AuthManager.is_admin() else "👤 User"
                right_cols[0].markdown(f'<div class="user-badge">{role_badge}: {user.get("full_name", user.get("username"))}</div>', unsafe_allow_html=True)
                
                # Logout button
                if right_cols[1].button("🚪", use_container_width=True):
                    AuthManager.logout()
                    st.session_state.current_page = "home"
                    st.rerun()
            
            # Theme toggle
            current_theme = UIManager.get_theme()
            theme_icon = "🌙" if current_theme == "light" else "☀️"
            if right_cols[0 if not AuthManager.is_authenticated() else 1].button(theme_icon, use_container_width=True):
                UIManager.toggle_theme()
                st.rerun()
        
        st.markdown("---")
        return st.session_state.current_page
    
    @staticmethod
    def _get_image_base64(image_path):
        """Convert image to base64 for inline display."""
        import base64
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    
    @staticmethod
    def render_header():
        """Deprecated - kept for compatibility."""
        pass
    
    @staticmethod
    def render_theme_toggle():
        """Deprecated - now in navbar."""
        pass
    
    @staticmethod
    def render_report_card(report):
        """Renders a custom styled card for a report."""
        status_color = "#00CC96" if report['status'] == 'Resolved' else "#FF4B4B"
        icon = "✅" if report['status'] == 'Resolved' else "⏳"
        
        # Handle both old 'type' and new 'category' fields
        category = report.get('category', report.get('type', 'N/A'))
        subcategory = report.get('subcategory', '')
        category_display = f"{category}" + (f" - {subcategory}" if subcategory else "")
        
        # Handle location display
        division = report.get('division', 'N/A')
        district = report.get('district', 'N/A')
        location_display = f"📍 {district}, {division}"
        
        st.markdown(
            f"""
            <div class="report-card" style="border-left-color: {status_color}">
                <h4 style="margin:0; color: white;">{icon} {report['title']} <span style="font-size: 0.8em; opacity: 0.7; float:right;">#{report['id']}</span></h4>
                <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #aaa;">
                    <b>{category_display}</b> | {report['date']} | Status: <b style="color:{status_color}">{report['status']}</b>
                </p>
                <p style="margin: 5px 0 0 0; font-size: 0.85em; color: #888;">
                    {location_display}
                </p>
                <p style="font-size: 0.9em; margin-top: 10px;">{report['description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
