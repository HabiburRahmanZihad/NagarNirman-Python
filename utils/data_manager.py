import streamlit as st
from datetime import datetime
import json
import os
import io
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

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

    @staticmethod
    def generate_reports_pdf(reports):
        """Generates a professional PDF document of reports."""
        if not FPDF:
            st.error("PDF generation library (fpdf2) is not installed.")
            return None
        
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Header
            pdf.set_font("Helvetica", "B", 24)
            pdf.set_text_color(42, 125, 47) # Brand Green
            pdf.cell(0, 20, "NagarNirman - System Report", ln=True, align="C")
            
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(100)
            pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
            pdf.ln(10)
            
            # Table Header
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_fill_color(240)
            pdf.cell(10, 10, "ID", 1, 0, "C", True)
            pdf.cell(60, 10, "Title", 1, 0, "C", True)
            pdf.cell(50, 10, "Category", 1, 0, "C", True)
            pdf.cell(30, 10, "Status", 1, 0, "C", True)
            pdf.cell(40, 10, "Date", 1, 1, "C", True)
            
            # Data Rows
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(0)
            for r in reports:
                # Ensure text fits or is truncated
                title = str(r['title'])[:30] + '...' if len(str(r['title'])) > 30 else str(r['title'])
                cat = str(r['category'])[:25]
                
                pdf.cell(10, 8, str(r['id']), 1, 0, "C")
                pdf.cell(60, 8, title, 1, 0, "L")
                pdf.cell(50, 8, cat, 1, 0, "L")
                pdf.cell(30, 8, str(r['status']), 1, 0, "C")
                pdf.cell(40, 8, str(r['date']), 1, 1, "C")
            
            # Footer summary
            pdf.ln(10)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, f"Total Reports: {len(reports)}", ln=True)

            # Ensure we return binary bytes for Streamlit's download_button
            # pdf.output(dest='S') may return str, bytes or bytearray depending
            # on the fpdf version. Normalize to bytes.
            out = pdf.output(dest='S')
            if isinstance(out, (bytes, bytearray)):
                return bytes(out)
            if isinstance(out, str):
                return out.encode('latin-1')
            return bytes(out)
        except Exception as e:
            st.error(f"Failed to generate PDF: {e}")
            return None
