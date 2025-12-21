import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager
from utils.location_data import get_divisions, get_categories

def show_admin_page():
    st.title("👮 Authority Dashboard")
    st.markdown("Manage and resolve reported issues efficiently.")
    
    reports = DataManager.get_all_reports()
    if not reports:
        st.info("No reports to manage.")
        return

    df = pd.DataFrame(reports)
    
    # Add filters for division, district, category, and status
    st.markdown("### 🔍 Filters")
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    # Get unique values for filters (handle reports without data)
    all_divisions = ["All"] + sorted(list(set([r.get("division", "N/A") for r in reports])))
    all_districts = ["All"] + sorted(list(set([r.get("district", "N/A") for r in reports])))
    all_categories = ["All"] + sorted(list(set([r.get("category", r.get("type", "N/A")) for r in reports])))
    all_statuses = ["All", "Pending", "In Progress", "Resolved", "Rejected"]
    
    selected_division = filter_col1.selectbox("Division", all_divisions)
    selected_district = filter_col2.selectbox("District", all_districts)
    selected_category = filter_col3.selectbox("Category", all_categories)
    selected_status = filter_col4.selectbox("Status", all_statuses)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_division != "All":
        filtered_df = filtered_df[filtered_df["division"] == selected_division]
    if selected_district != "All":
        filtered_df = filtered_df[filtered_df["district"] == selected_district]
    if selected_category != "All":
        # Handle both old 'type' and new 'category' field
        if "category" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["category"] == selected_category]
        elif "type" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["type"] == selected_category]
    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["status"] == selected_status]
    
    st.markdown("---")
    
    # Display summary stats
    st.markdown("### 📈 Summary")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    total_reports = len(filtered_df)
    pending = len(filtered_df[filtered_df["status"] == "Pending"]) if "status" in filtered_df.columns else 0
    in_progress = len(filtered_df[filtered_df["status"] == "In Progress"]) if "status" in filtered_df.columns else 0
    resolved = len(filtered_df[filtered_df["status"] == "Resolved"]) if "status" in filtered_df.columns else 0
    
    stat_col1.metric("Total Reports", total_reports)
    stat_col2.metric("Pending", pending)
    stat_col3.metric("In Progress", in_progress)
    stat_col4.metric("Resolved", resolved)
    
    st.markdown("---")

    # Tabs for organization
    tab1, tab2 = st.tabs(["📊 Data Overview", "🛠️ Action Center"])

    with tab1:
        # Determine which columns exist and reorder
        possible_columns = ["id", "title", "category", "subcategory", "type", "division", "district", "status", "date", "lat", "lon", "description"]
        display_columns = [col for col in possible_columns if col in filtered_df.columns]
        
        # Remove 'type' if 'category' exists (avoid redundancy)
        if "category" in display_columns and "type" in display_columns:
            display_columns.remove("type")
        
        display_df = filtered_df[display_columns] if display_columns else filtered_df
        
        st.dataframe(
            display_df, 
            use_container_width=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "title": st.column_config.TextColumn("Title", width="medium"),
                "category": st.column_config.TextColumn("Category", width="medium"),
                "subcategory": st.column_config.TextColumn("Subcategory", width="medium"),
                "type": st.column_config.TextColumn("Type", width="small"),
                "division": st.column_config.TextColumn("Division", width="medium"),
                "district": st.column_config.TextColumn("District", width="medium"),
                "lat": st.column_config.NumberColumn("Latitude", format="%.4f", width="small"),
                "lon": st.column_config.NumberColumn("Longitude", format="%.4f", width="small"),
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Pending", "In Progress", "Resolved", "Rejected"],
                    disabled=True
                ),
                "date": st.column_config.TextColumn("Date", width="small"),
                "description": st.column_config.TextColumn("Description", width="large")
            }
        )

    with tab2:
        st.subheader("Update Issue Status")
        
        col_select, col_action, col_btn = st.columns([3, 2, 1])
        
        # Dropdown options with full details
        def get_report_label(r):
            location = f"{r.get('district', 'N/A')}, {r.get('division', 'N/A')}"
            category = r.get('category', r.get('type', 'N/A'))
            return f"#{r['id']} {r['title']} | {location} | {category} ({r['status']})"
        
        options = {get_report_label(r): r['id'] for r in reports}
        selected_option = col_select.selectbox("Select Report", options.keys())
        
        if selected_option:
            selected_id = options[selected_option]
            new_status = col_action.selectbox("Set New Status", ["Pending", "In Progress", "Resolved", "Rejected"])
            
            st.markdown(" ")
            if col_btn.button("Update Status", use_container_width=True):
                if DataManager.update_status(selected_id, new_status):
                    st.success(f"Report #{selected_id} updated to {new_status}")
                    st.rerun()
                else:
                    st.error("Failed to update status.")

    st.markdown("---")
    st.subheader("📥 Export Data")
    
    try:
        from utils.report_generator import ReportGenerator
        
        if st.button("Generate PDF Report"):
            pdf_bytes = ReportGenerator.generate_pdf(reports)
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"nagarnirman_reports_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
    except ImportError:
        st.info("PDF export module not available.")
