import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.auth_manager import AuthManager
from utils.ui_manager import UIManager

def show_my_reports_page():
    """Display the current user's submitted reports with Boss Level UI."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("📋 My Submissions")
    
    if not AuthManager.is_authenticated():
        st.warning("Please login to view your reports.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
        
    current_user = AuthManager.get_current_user()
    username = current_user.get('username')

    # Use DataManager helper which filters by 'submitted_by' to match how
    # reports are stored when created via `DataManager.add_report()`.
    my_reports = DataManager.get_reports_by_user(username)
    
    if not my_reports:
        st.info("You haven't submitted any reports yet.")
        if st.button("🚀 Submit Your First Report"):
            st.session_state.current_page = "submit_report"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Tabs for different views
    tab_card, tab_table = st.tabs(["🗂️ Card View", "📊 Data Table"])
    
    with tab_card:
        st.markdown('<div class="mt-4">', unsafe_allow_html=True)
        UIManager.render_report_cards_grid(list(reversed(my_reports)), columns=4)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_table:
        st.markdown('<div class="glass-card mt-4">', unsafe_allow_html=True)
        df = pd.DataFrame(my_reports)
        # Reorder and rename columns for display
        cols = ['id', 'title', 'category', 'date', 'status', 'division', 'district']
        df_display = df[cols].copy()
        df_display.columns = [c.capitalize() for c in cols]
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
