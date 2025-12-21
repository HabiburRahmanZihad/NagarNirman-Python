import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.auth_manager import AuthManager
from utils.ui_manager import UIManager

def show_my_reports_page():
    """Display the current user's submitted reports."""
    st.title("📋 My Reports")
    st.markdown("View and track your submitted reports.")
    
    # Get current user
    current_user = AuthManager.get_current_user()
    if not current_user:
        st.error("You must be logged in to view your reports.")
        return
    
    username = current_user.get('username')
    
    # Get user's reports
    my_reports = DataManager.get_reports_by_user(username)
    
    if not my_reports:
        st.info("You haven't submitted any reports yet. Go to 'Submit Report' to report an issue!")
        return
    
    # Display summary stats
    st.markdown("### 📊 Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(my_reports)
    pending = sum(1 for r in my_reports if r.get("status") == "Pending")
    in_progress = sum(1 for r in my_reports if r.get("status") == "In Progress")
    resolved = sum(1 for r in my_reports if r.get("status") == "Resolved")
    
    col1.metric("Total Reports", total)
    col2.metric("⏳ Pending", pending)
    col3.metric("🔧 In Progress", in_progress)
    col4.metric("✅ Resolved", resolved)
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📊 Table View", "📝 Card View"])
    
    with tab1:
        # Dataframe view
        df = pd.DataFrame(my_reports)
        
        # Reorder columns
        column_order = ["id", "title", "category", "subcategory", "division", "district", "status", "date", "description"]
        display_columns = [col for col in column_order if col in df.columns]
        display_df = df[display_columns]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "title": st.column_config.TextColumn("Title", width="medium"),
                "category": st.column_config.TextColumn("Category", width="medium"),
                "subcategory": st.column_config.TextColumn("Subcategory", width="medium"),
                "division": st.column_config.TextColumn("Division", width="small"),
                "district": st.column_config.TextColumn("District", width="small"),
                "status": st.column_config.TextColumn("Status", width="small"),
                "date": st.column_config.TextColumn("Date", width="small"),
                "description": st.column_config.TextColumn("Description", width="large")
            }
        )
    
    with tab2:
        # Card view
        st.markdown("### Recent Reports")
        UIManager.render_report_cards_grid(list(reversed(my_reports)), columns=4)
