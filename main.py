import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP & CONFIGURATION
st.set_page_config(page_title="NagarNirman", page_icon="🏗️", layout="wide")

# Initialize "Database" in Session State (Ram)
if 'reports' not in st.session_state:
    st.session_state.reports = [
        # Sample Data
        {
            "id": 1,
            "title": "Broken Road at GEC",
            "type": "Road",
            "status": "Pending",
            "lat": 22.3569,
            "lon": 91.8232,
            "date": "2025-12-18",
            "description": "Deep pothole causing traffic."
        },
        {
            "id": 2,
            "title": "Garbage in Nasirabad",
            "type": "Waste",
            "status": "Resolved",
            "lat": 22.3650,
            "lon": 91.8200,
            "date": "2025-12-19",
            "description": "Waste piled up for 3 days."
        }
    ]

# 2. SIDEBAR NAVIGATION
st.sidebar.image("https://img.icons8.com/color/96/city.png", width=80)
st.sidebar.title("NagarNirman 🏗️")
menu = st.sidebar.radio("Navigation", ["Home & Map", "Submit Report", "Admin Dashboard"])

# 3. PAGE: HOME & MAP
if menu == "Home & Map":
    st.title("🌆 City Overview")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    total = len(st.session_state.reports)
    resolved = sum(1 for r in st.session_state.reports if r["status"] == "Resolved")
    pending = total - resolved
    
    col1.metric("Total Reports", total)
    col2.metric("Resolved", resolved, delta_color="normal")
    col3.metric("Pending", pending, delta_color="inverse")

    st.divider()

    # Map Visualization
    st.subheader("📍 Issue Map")
    if st.session_state.reports:
        df = pd.DataFrame(st.session_state.reports)
        # Streamlit map requires 'lat' and 'lon' columns
        st.map(df, zoom=13, size=200, color="#FF4B4B")
    else:
        st.info("No reports to show on map.")

    # Recent Reports List
    st.subheader("📝 Recent Reports")
    for report in st.session_state.reports:
        with st.expander(f"{'✅' if report['status']=='Resolved' else '⏳'} {report['title']} ({report['date']})"):
            st.write(f"**Type:** {report['type']}")
            st.write(f"**Status:** {report['status']}")
            st.write(f"**Description:** {report['description']}")
            st.caption(f"Location: {report['lat']}, {report['lon']}")

# 4. PAGE: SUBMIT REPORT
elif menu == "Submit Report":
    st.title("📢 Report an Issue")
    st.write("Help us fix the city by reporting infrastructure problems.")
    
    with st.form("report_form"):
        title = st.text_input("Issue Title", placeholder="e.g., Broken Street Light")
        type_option = st.selectbox("Problem Type", ["Road", "Water", "Electricity", "Waste", "Other"])
        desc = st.text_area("Description")
        
        col_lat, col_lon = st.columns(2)
        # Defaulting to Chittagong coordinates
        lat = col_lat.number_input("Latitude", value=22.3569, format="%.4f")
        lon = col_lon.number_input("Longitude", value=91.7832, format="%.4f")
        
        uploaded_file = st.file_uploader("Upload Evidence (Image)", type=['png', 'jpg'])
        
        submitted = st.form_submit_button("Submit Report")
        
        if submitted:
            if title and desc:
                new_id = len(st.session_state.reports) + 1
                new_report = {
                    "id": new_id,
                    "title": title,
                    "type": type_option,
                    "status": "Pending",
                    "lat": lat,
                    "lon": lon,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "description": desc
                }
                st.session_state.reports.append(new_report)
                st.success("Report submitted successfully! Thank you for your contribution.")
            else:
                st.error("Please fill in the title and description.")

# 5. PAGE: ADMIN DASHBOARD
elif menu == "Admin Dashboard":
    st.title("👮 Authority Dashboard")
    st.write("Manage and resolve reported issues.")
    
    # Convert list to DataFrame for easier editing
    df = pd.DataFrame(st.session_state.reports)
    
    # Data Editor (Editable Table)
    st.subheader("Manage Reports")
    
    # Display statistics
    if not df.empty:
        # Create tabs for filtering
        tab1, tab2 = st.tabs(["All Reports", "Pending Only"])
        
        with tab1:
            st.dataframe(df)
            
        with tab2:
            pending_df = df[df["status"] == "Pending"]
            st.dataframe(pending_df)
            
        st.divider()
        
        # Action Area
        st.subheader("Update Status")
        col_select, col_action, col_btn = st.columns([2, 1, 1])
        
        options = {f"{r['id']} - {r['title']}": r['id'] for r in st.session_state.reports}
        selected_option = col_select.selectbox("Select Report ID", options.keys())
        
        if selected_option:
            selected_id = options[selected_option]
            new_status = col_action.selectbox("Set Status", ["Pending", "In Progress", "Resolved", "Rejected"])
            
            if col_btn.button("Update"):
                # Find and update the report in the list
                for r in st.session_state.reports:
                    if r['id'] == selected_id:
                        r['status'] = new_status
                        st.success(f"Report #{selected_id} updated to {new_status}")
                        st.rerun() # Refresh page to show changes
    else:
        st.info("No reports available.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 NagarNirman | Built with Python 🐍")