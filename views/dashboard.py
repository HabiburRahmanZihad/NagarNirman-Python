import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.ui_manager import UIManager

def show_dashboard():
    st.title("🌆 City Overview")
    
    reports = DataManager.get_all_reports()
    
    # Validation for Empty Data
    if not reports:
        st.info("No data available yet.")
        return

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    total = len(reports)
    resolved = sum(1 for r in reports if r["status"] == "Resolved")
    pending = total - resolved
    
    col1.metric("Total Reports", total)
    col2.metric("Resolved", resolved, delta_color="normal")
    col3.metric("Pending", pending, delta_color="inverse")

    st.markdown("---")

    # Map Section
    st.subheader("📍 Issue Map")
    df = pd.DataFrame(reports)
    # Streamlit map requires lat/lon col names
    st.map(df, zoom=12, size=50, color="#FF4B4B") # Using 'size' requires numeric column or static int, here static.

    # Recent Reports
    st.subheader("📝 Recent Reports")
    # Show all reports in grid format (4 columns)
    UIManager.render_report_cards_grid(list(reversed(reports)), columns=4)
