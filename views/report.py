import streamlit as st
from utils.data_manager import DataManager
from utils.auth_manager import AuthManager
from utils.location_data import (
    get_divisions, get_districts, get_district_coordinates,
    get_categories, get_subcategories
)

def show_report_page():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("📢 Report an Issue")
    st.markdown("Help us fix the city by reporting infrastructure problems below.")
    
    # Division and District Selection
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📍 Administrative Location")
    col_div, col_dist = st.columns(2)
    
    divisions = get_divisions()
    selected_division = col_div.selectbox("Division", divisions, key="division_select")
    
    districts = get_districts(selected_division)
    selected_district = col_dist.selectbox("District", districts, key="district_select")
    
    lat, lon = get_district_coordinates(selected_division, selected_district)
    if lat is None:
        lat, lon = 22.3569, 91.7832
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Category and Subcategory Selection
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📂 Issue Category")
    col_cat, col_subcat = st.columns(2)
    
    categories = get_categories()
    selected_category = col_cat.selectbox("Category", categories, key="category_select")
    
    subcategories = get_subcategories(selected_category)
    selected_subcategory = col_subcat.selectbox("Subcategory", subcategories, key="subcategory_select")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Form for the rest of the details
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.form("report_form", clear_on_submit=True):
        st.markdown("### 📝 Issue Details")
        title = st.text_input("Issue Title", placeholder="e.g., Broken Street Light at 5th Ave")
        desc = st.text_area("Description", placeholder="Describe the issue in detail...")
        
        st.markdown('<div class="mt-4">', unsafe_allow_html=True)
        st.markdown("#### 🌍 Geographic Coordinates")
        st.caption(f"Auto-filled based on {selected_district}. Adjust if necessary.")
        col1, col2 = st.columns(2)
        input_lat = col1.number_input("Latitude", value=lat, format="%.4f")
        input_lon = col2.number_input("Longitude", value=lon, format="%.4f")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="mt-4">', unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Submit Official Report", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submitted:
            if title and desc and selected_division and selected_district and selected_category:
                current_user = AuthManager.get_current_user()
                username = current_user.get('username') if current_user else None
                
                new_id = DataManager.add_report(
                    title=title,
                    category=selected_category,
                    subcategory=selected_subcategory,
                    desc=desc,
                    division=selected_division,
                    district=selected_district,
                    lat=input_lat,
                    lon=input_lon,
                    username=username
                )
                st.success(f"✅ Report #{new_id} submitted successfully!")
                st.balloons()
            else:
                st.error("Please fill in all required fields.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
