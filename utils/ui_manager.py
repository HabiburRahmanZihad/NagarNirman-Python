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
        """Loads custom CSS and handles theme switching via direct variable injection."""
        theme = UIManager.get_theme()
        
        # Define theme variables in Python for reliable injection
        if theme == 'light':
            vars_css = """
                :root {
                    --color-primary: #004540;
                    --color-secondary: #2a7d2f;
                    --color-accent: #f2a921;
                    --color-neutral: #6B7280;
                    --color-base-100: #FFFFFF;
                    --color-base-200: #F3F4F6;
                    --color-base-300: #F6FFF9;
                    --color-info: #002E2E;
                    --color-warning: #fbbf24;
                    --color-success: #81d586;
                    --text-color: #1a1a1a;
                    --text-muted: #666666;
                    --card-bg: rgba(255, 255, 255, 0.95);
                    --border-color: rgba(0, 0, 0, 0.1);
                    --shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                }
            """
        else:
            vars_css = """
                :root {
                    --color-primary: #2a7d2f;
                    --color-secondary: #9ad83e;
                    --color-accent: #ffcc33;
                    --color-neutral: #E5E7EB;
                    --color-base-100: #0f1a16;
                    --color-base-200: #1b2a25;
                    --color-base-300: #243832;
                    --color-info: #D1FAE5;
                    --color-warning: #fbbf24;
                    --color-success: #81d586;
                    --text-color: #E0E0E0;
                    --text-muted: #aaaaaa;
                    --card-bg: rgba(255, 255, 255, 0.03);
                    --border-color: rgba(255, 255, 255, 0.1);
                    --shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                }
            """

        # Load base CSS from file
        base_css = ""
        if os.path.exists(file_path):
            with open(file_path) as f:
                base_css = f.read()
        
        # Inject theme variables and combined CSS
        # IMPORTANT: No leading whitespace for the style tag to avoid markdown parsing issues
        st.markdown(f"<style>\n{vars_css}\n{base_css}\n</style>", unsafe_allow_html=True)

    
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
            <div class="report-card {'resolved' if report['status'] == 'Resolved' else ''}">
                <h4 style="margin:0;">{icon} {report['title']} <span style="font-size: 0.8em; opacity: 0.7; float:right;">#{report['id']}</span></h4>
                <p style="margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.8;">
                    <b>{category_display}</b> | {report['date']} | Status: <b>{report['status']}</b>
                </p>
                <p style="margin: 5px 0 0 0; font-size: 0.85em; opacity: 0.7;">
                    {location_display}
                </p>
                <p style="font-size: 0.9em; margin-top: 10px;">{report['description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    @staticmethod
    def render_report_cards_grid(reports, columns=4):
        """Renders report cards in a grid format with specified number of columns."""
        if not reports:
            st.info("No reports to display.")
            return
        
        # Process reports in batches of 'columns' count
        for i in range(0, len(reports), columns):
            # Create a row with the specified number of columns
            cols = st.columns(columns)
            
            # Fill each column with a report card
            for j, col in enumerate(cols):
                report_index = i + j
                if report_index < len(reports):
                    with col:
                        report = reports[report_index]
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
                            <div class="report-card-grid {'resolved' if report['status'] == 'Resolved' else ''}">
                                <h4 style="margin:0; font-size: 1em;">{icon} {report['title']} <span style="font-size: 0.7em; opacity: 0.7; float:right;">#{report['id']}</span></h4>
                                <p style="margin: 5px 0 0 0; font-size: 0.75em; opacity: 0.8;">
                                    <b>{category_display}</b>
                                </p>
                                <p style="margin: 3px 0 0 0; font-size: 0.7em; opacity: 0.7;">
                                    {report['date']} | <b>{report['status']}</b>
                                </p>
                                <p style="margin: 3px 0 0 0; font-size: 0.7em; opacity: 0.7;">
                                    {location_display}
                                </p>
                                <p style="font-size: 0.75em; margin-top: 8px; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">{report['description']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
