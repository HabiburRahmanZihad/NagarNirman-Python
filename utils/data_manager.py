import streamlit as st
from datetime import datetime
import json
import os

class DataManager:
    DB_FILE = "reports_db.json"
    
    @staticmethod
    def _load_from_file():
        """Load reports from JSON file."""
        if os.path.exists(DataManager.DB_FILE):
            try:
                with open(DataManager.DB_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, return default data
                return DataManager._get_default_data()
        else:
            return DataManager._get_default_data()
    
    @staticmethod
    def _save_to_file(reports):
        """Save reports to JSON file."""
        try:
            with open(DataManager.DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(reports, f, indent=2, ensure_ascii=False)
        except IOError as e:
            st.error(f"Failed to save data: {e}")
    
    @staticmethod
    def _get_default_data():
        """Return default sample data."""
        return [
            {
                "id": 1,
                "title": "Broken Road at GEC",
                "category": "Road & Infrastructure Issues",
                "subcategory": "Potholes",
                "status": "Pending",
                "division": "Chittagong",
                "district": "Chittagong",
                "lat": 22.3569,
                "lon": 91.8232,
                "date": "2025-12-18",
                "description": "Deep pothole causing traffic congestion near the intersection."
            },
            {
                "id": 2,
                "title": "Garbage Pile in Nasirabad",
                "category": "Garbage & Sanitation",
                "subcategory": "Overflowing garbage bins",
                "status": "Resolved",
                "division": "Chittagong",
                "district": "Chittagong",
                "lat": 22.3650,
                "lon": 91.8200,
                "date": "2025-12-19",
                "description": "Waste piled up for 3 days obstructing the sidewalk."
            }
        ]
    
    @staticmethod
    def init_db():
        """Initialize the 'database' in session state if not exists."""
        if 'reports' not in st.session_state:
            # Load from file or use defaults
            st.session_state.reports = DataManager._load_from_file()

    @staticmethod
    def get_all_reports():
        return st.session_state.reports

    @staticmethod
    def add_report(title, category, subcategory, desc, division, district, lat, lon, username=None):
        # Generate new ID based on max existing ID
        existing_ids = [r['id'] for r in st.session_state.reports] if st.session_state.reports else [0]
        new_id = max(existing_ids) + 1
        
        new_report = {
            "id": new_id,
            "title": title,
            "category": category,
            "subcategory": subcategory,
            "status": "Pending",
            "division": division,
            "district": district,
            "lat": lat,
            "lon": lon,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": desc,
            "submitted_by": username  # Track who submitted the report
        }
        st.session_state.reports.append(new_report)
        
        # Save to file immediately
        DataManager._save_to_file(st.session_state.reports)
        return new_id

    @staticmethod
    def update_status(report_id, new_status):
        for r in st.session_state.reports:
            if r['id'] == report_id:
                r['status'] = new_status
                # Save to file immediately
                DataManager._save_to_file(st.session_state.reports)
                return True
        return False

    @staticmethod
    def get_reports_by_user(username):
        """Get all reports submitted by a specific user."""
        if not username:
            return []
        return [r for r in st.session_state.reports if r.get('submitted_by') == username]
