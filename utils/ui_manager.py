import streamlit as st
import os
import textwrap

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
                    --color-background: #FFFFFF;
                    --color-surface: #F3F4F6;
                    --color-surface-brighter: #F6FFF9;
                    --color-info: #002E2E;
                    --color-warning: #fbbf24;
                    --color-success: #81d586;
                    --text-primary: #1a1a1a;
                    --text-secondary: #666666;
                    --card-bg: rgba(255, 255, 255, 0.7);
                    --glass-bg: rgba(255, 255, 255, 0.4);
                    --glass-border: rgba(255, 255, 255, 0.3);
                    --border-color: rgba(0, 0, 0, 0.05);
                    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
                    --shadow-md: 0 6px 12px rgba(0, 0, 0, 0.08);
                    --shadow-lg: 0 12px 24px rgba(0, 0, 0, 0.12);
                    
                    /* Spacing Grit System */
                    --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
                    --space-5: 20px; --space-6: 24px; --space-8: 32px; --space-10: 40px;
                    --radius-sm: 8px; --radius-md: 12px; --radius-lg: 20px;
                }
            """
        else:
            vars_css = """
                :root {
                    --color-primary: #2a7d2f;
                    --color-secondary: #9ad83e;
                    --color-accent: #ffcc33;
                    --color-neutral: #E5E7EB;
                    --color-background: #0d1512;
                    --color-surface: #15231e;
                    --color-surface-brighter: #1c2e28;
                    --color-info: #D1FAE5;
                    --color-warning: #fbbf24;
                    --color-success: #81d586;
                    --text-primary: #f0f0f0;
                    --text-secondary: #aaaaaa;
                    --card-bg: rgba(30, 45, 40, 0.5);
                    --glass-bg: rgba(18, 30, 25, 0.65);
                    --glass-border: rgba(255, 255, 255, 0.15);
                    --border-color: rgba(255, 255, 255, 0.05);
                    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.2);
                    --shadow-md: 0 6px 16px rgba(0, 0, 0, 0.4);
                    --shadow-lg: 0 16px 32px rgba(0, 0, 0, 0.5);
                    
                    /* Spacing Grit System */
                    --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
                    --space-5: 20px; --space-6: 24px; --space-8: 32px; --space-10: 40px;
                    --radius-sm: 8px; --radius-md: 12px; --radius-lg: 20px;
                }
            """

        # Load base CSS from file
        base_css = ""
        if os.path.exists(file_path):
            with open(file_path) as f:
                base_css = f.read()
        
        # Session Persistence JS
        # This script syncs the session token to/from localStorage
        session_token = st.session_state.get('session_token', '')
        is_authenticated = st.session_state.get('authenticated', False)
        
        sync_js = f"""
<script>
    (function() {{
        const token = '{session_token}';
        const isAuthenticated = {str(is_authenticated).lower()};
        const currentUrl = new URL(window.location.href);
        const hasTokenInUrl = currentUrl.searchParams.has('st_token');
        const isLogoutFlow = currentUrl.searchParams.has('logout');

        // 1. If we have a logout flag, clear everything
        if (isLogoutFlow) {{
            console.log('Clearing session due to logout flag');
            localStorage.removeItem('nn_session_token');
            currentUrl.searchParams.delete('logout');
            currentUrl.searchParams.delete('st_token');
            window.location.href = currentUrl.toString();
            return;
        }}

        // 2. If authenticated, make sure the token is in localStorage
        if (isAuthenticated && token) {{
            if (localStorage.getItem('nn_session_token') !== token) {{
                console.log('Syncing token to localStorage');
                localStorage.setItem('nn_session_token', token);
            }}
            // Clean up the URL if needed
            if (hasTokenInUrl) {{
                currentUrl.searchParams.delete('st_token');
                window.history.replaceState({{}}, '', currentUrl.toString());
            }}
        }} 
        // 3. If NOT authenticated, try to restore from localStorage
        else if (!isAuthenticated) {{
            const storedToken = localStorage.getItem('nn_session_token');
            if (storedToken && !hasTokenInUrl) {{
                console.log('Restoring session from localStorage');
                currentUrl.searchParams.set('st_token', storedToken);
                window.location.href = currentUrl.toString();
            }}
        }}
    }})();
</script>
"""

        # Inject theme variables, combined CSS and sync JS
        # IMPORTANT: No leading whitespace for the style tag to avoid markdown parsing issues
        st.markdown(f"{sync_js}\n<style>\n{vars_css}\n{base_css}\n</style>", unsafe_allow_html=True)

    
    @staticmethod
    def render_navbar():
        """Renders the top navigation bar with Boss Level styling."""
        from utils.auth_manager import AuthManager
        
        # Initialize current page in session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'

        # Custom Navbar CSS (scoped to avoid collisions)
        st.markdown("""
            <style>
            .st-emotion-cache-1835u59 { padding-top: 0; }
            .navbar-container {
                padding: var(--space-3) var(--space-6);
                background: var(--glass-bg);
                backdrop-filter: blur(20px) saturate(180%);
                -webkit-backdrop-filter: blur(20px) saturate(180%);
                border-bottom: 1px solid var(--glass-border);
                margin-bottom: var(--space-4);
                border-radius: 0 0 var(--radius-md) var(--radius-md);
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            }
            .brand-wrapper {
                display: flex;
                align-items: center;
                gap: var(--space-3);
            }
            .brand-logo {
                height: 40px;
                width: auto;
            }
            </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            col_brand, col_nav, col_auth = st.columns([2.5, 5, 2.5])
            
            with col_brand:
                logo_path = "logo/logo.png"
                if os.path.exists(logo_path):
                    st.markdown(f"""
                        <div class="brand-wrapper">
                            <img src="data:image/png;base64,{UIManager._get_image_base64(logo_path)}" class="brand-logo">
                            <div class="navbar-brand">NagarNirman</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="navbar-brand">🏙️ NagarNirman</div>', unsafe_allow_html=True)
            
            with col_nav:
                is_auth = AuthManager.is_authenticated()
                is_admin = AuthManager.is_admin()
                
                # Dynamic column count based on visibility
                visible_items = ["Home", "About"]
                if is_auth and not is_admin: 
                    visible_items.extend(["Report", "My Reports"])
                if is_admin: 
                    visible_items.append("Admin Dashboard")
                # If only a single nav item (e.g., guest: only Home), create
                # spacer columns to center the button and avoid a full-width button.
                if len(visible_items) == 1:
                    nav_cols = st.columns([1, 2, 1])
                    curr_col = 1
                else:
                    nav_cols = st.columns(len(visible_items))
                    curr_col = 0

                # 1. Home (Always visible)
                if nav_cols[curr_col].button("🏠 Home", use_container_width=True, key="nav_home",
                                     type="primary" if st.session_state.current_page == "home" else "secondary"):
                    st.session_state.current_page = "home"
                    st.rerun()
                curr_col += 1

                # 1b. About (Always visible)
                if nav_cols[curr_col].button("ℹ️ About", use_container_width=True, key="nav_about",
                                     type="primary" if st.session_state.current_page == "about" else "secondary"):
                    st.session_state.current_page = "about"
                    st.rerun()
                curr_col += 1
                
                # 2. User-specific Routes (Only for non-admin users)
                if is_auth and not is_admin:
                    if nav_cols[curr_col].button("📢 Make Report", use_container_width=True, key="nav_report",
                                         type="primary" if st.session_state.current_page == "submit_report" else "secondary"):
                        st.session_state.current_page = "submit_report"
                        st.rerun()
                    curr_col += 1
                    
                    if nav_cols[curr_col].button("📋 My Reports", use_container_width=True, key="nav_my",
                                         type="primary" if st.session_state.current_page == "my_reports" else "secondary"):
                        st.session_state.current_page = "my_reports"
                        st.rerun()
                    curr_col += 1

                # 3. Admin Route
                if is_admin:
                    if nav_cols[curr_col].button("🛡️ Admin Dashboard", use_container_width=True, key="nav_admin",
                                         type="primary" if st.session_state.current_page == "admin" else "secondary"):
                        st.session_state.current_page = "admin"
                        st.rerun()

            with col_auth:
                right_cols = st.columns([1.5, 0.7, 1.2])
                
                # Theme toggle
                current_theme = UIManager.get_theme()
                theme_icon = "🌙" if current_theme == "light" else "☀️"
                if right_cols[1].button(theme_icon, use_container_width=True, key="theme_toggle"):
                    UIManager.toggle_theme()
                    st.rerun()

                if not AuthManager.is_authenticated():
                    if right_cols[0].button("🔐", use_container_width=True, key="nav_login", help="Login"):
                        st.session_state.current_page = "login"
                        st.rerun()
                else:
                    user = AuthManager.get_current_user()
                    username = user.get("full_name", user.get("username", "User"))
                    
                    if right_cols[0].button(f"👤 {username}", use_container_width=True, key="profile_btn", 
                                            type="primary" if st.session_state.get('show_profile') else "secondary"):
                        st.session_state.show_profile = not st.session_state.get('show_profile', False)
                    
                    if right_cols[2].button("🚪 Logout", use_container_width=True, key="logout_btn"):
                        AuthManager.logout()
                        st.session_state.current_page = "home"
                        st.session_state.show_profile = False
                        st.query_params['logout'] = 'true'
                        st.rerun()
                
            # Render Profile Details if toggled
            if st.session_state.get('show_profile', False) and AuthManager.is_authenticated():
                user = AuthManager.get_current_user()
                with st.expander("👤 User Profile Details", expanded=True):
                    p_col1, p_col2 = st.columns(2)
                    p_col1.markdown(f"**Full Name:** {user.get('full_name', 'N/A')}")
                    p_col1.markdown(f"**Username:** {user.get('username', 'N/A')}")
                    role = user.get('role', 'user')
                    p_col2.markdown(f"**Role:** {str(role).capitalize() if role else 'User'}")
                    if st.button("Close Profile", use_container_width=True):
                        st.session_state.show_profile = False
                        st.rerun()
        
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
        """Renders a custom styled card for a report with Boss Level aesthetics."""
        icon = "✅" if report['status'] == 'Resolved' else "⏳"
        
        # Handle both old 'type' and new 'category' fields
        category = report.get('category', report.get('type', 'N/A'))
        subcategory = report.get('subcategory', '')
        category_display = f"{category}" + (f" - {subcategory}" if subcategory else "")
        
        # Handle location display
        division = report.get('division', 'N/A')
        district = report.get('district', 'N/A')
        location_display = f"📍 {district}, {division}"

        card_html = f"""
<div class="report-card fade-in {'resolved' if report['status'] == 'Resolved' else ''}">
    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <h4 style="margin:0; font-size:1.1rem;">{icon} {report['title']}</h4>
        <span style="font-size: 0.8rem; font-weight:600; background:var(--border-color); padding:2px 8px; border-radius:4px; opacity:0.8;">#{report['id']}</span>
    </div>
    <div style="margin-top:var(--space-2); font-size: 0.85rem; opacity: 0.9;">
        <b style="color:var(--color-primary);">{category_display}</b> | {report['date']}
    </div>
    <div style="margin-top:1px; font-size: 0.8rem; opacity: 0.7;">
        {location_display} | <b>{report['status']}</b>
    </div>
    <p style="font-size: 0.9rem; margin-top: var(--space-4); border-top:1px solid var(--border-color); padding-top:var(--space-2);">{report['description']}</p>
</div>
"""
        st.markdown(textwrap.dedent(card_html).strip(), unsafe_allow_html=True)
    
    @staticmethod
    def render_report_cards_grid(reports, columns=4):
        """Renders report cards in a grid format with Boss Level aesthetics."""
        if not reports:
            st.info("No reports to display.")
            return
        # Render as a single responsive HTML grid to keep card heights uniform
        cards_html = ['<div class="cards-grid">']
        for report in reports:
            icon = "✅" if report['status'] == 'Resolved' else "⏳"
            category = report.get('category', report.get('type', 'N/A'))
            subcategory = report.get('subcategory', '')
            category_display = f"{category}" + (f" - {subcategory}" if subcategory else "")
            location_display = f"{report.get('district', 'N/A')}, {report.get('division', 'N/A')}"

            card = f'''
<div class="card-item">
    <div class="report-card-grid fade-in {'resolved' if report['status'] == 'Resolved' else ''}">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <h4 style="margin:0; font-size: 0.95rem; line-height:1.3;">{icon} {report['title']}</h4>
            <span style="font-size: 0.65rem; font-weight:600; opacity: 0.6;">#{report['id']}</span>
        </div>
        <div style="margin-top:auto; padding-top: var(--space-3);">
            <p style="margin:0; font-size: 0.75rem; font-weight:600; color:var(--color-primary);">{category_display}</p>
            <p style="margin:0; font-size: 0.7rem; opacity:0.7;">{report['date']} | {location_display}</p>
            <div style="margin-top:var(--space-2); font-size: 0.8rem; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                {report['description']}
            </div>
        </div>
    </div>
</div>
'''
            # Remove leading indentation so Markdown doesn't treat HTML as a code block
            cards_html.append(textwrap.dedent(card).strip())
        cards_html.append('</div>')

        st.markdown('\n'.join(cards_html), unsafe_allow_html=True)

    @staticmethod
    def render_footer():
        """Renders a simple, elegant 'Boss Level' footer with logo."""
        logo_path = "logo/logo.png"
        logo_html = ""
        if os.path.exists(logo_path):
            logo_html = f'<img src="data:image/png;base64,{UIManager._get_image_base64(logo_path)}" style="height:50px; vertical-align:middle; margin-right:10px; width:250px;">'
        footer_html = textwrap.dedent(f"""
        <div class="footer-container" style="text-align:center;">
            <div class="navbar-brand">
                {logo_html}
            </div>
            <div class="footer-bottom" style="margin-top:var(--space-4); border:none; padding:0;">
                &copy; 2025 NagarNirman | Designed for the Future of Urban Living
            </div>
        </div>
        """).strip()

        st.markdown(footer_html, unsafe_allow_html=True)

    @staticmethod
    def render_custom_metric(label, value, icon=""):
        """Renders a WOW-level custom metric card."""
        metric_html = textwrap.dedent(f"""
        <div class="wow-card metric-container">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """).strip()

        st.markdown(metric_html, unsafe_allow_html=True)

    @staticmethod
    def render_wow_card(content_html):
        """Wraps HTML content in a WOW card."""
        # Ensure the inner content has no leading indentation so Markdown
        # doesn't interpret it as a code block.
        inner = textwrap.dedent(content_html).strip()
        wrapper = f"""
    <div class="wow-card">
    {inner}
    </div>
    """
        st.markdown(textwrap.dedent(wrapper).strip(), unsafe_allow_html=True)
