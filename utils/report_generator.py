from fpdf import FPDF
import tempfile
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_pdf(reports):
        """Generates a PDF file from a list of reports and returns the byte content."""
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "NagarNirman - City Issues Report", ln=True, align="C")
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        pdf.ln(10)
        
        # Table Header
        pdf.set_font("Arial", "B", 10)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(15, 10, "ID", 1, 0, 'C', 1)
        pdf.cell(50, 10, "Title", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Type", 1, 0, 'C', 1)
        pdf.cell(30, 10, "Status", 1, 0, 'C', 1)
        pdf.cell(65, 10, "Date", 1, 1, 'C', 1)
        
        # Table Body
        pdf.set_font("Arial", "", 9)
        for report in reports:
            # Shorten title if too long
            title = (report['title'][:25] + '...') if len(report['title']) > 25 else report['title']
            
            pdf.cell(15, 10, str(report['id']), 1)
            pdf.cell(50, 10, title, 1)
            pdf.cell(30, 10, report['type'], 1)
            
            # Color code status (Text color only for simplicity in basic FPDF)
            pdf.cell(30, 10, report['status'], 1)
            pdf.cell(65, 10, report['date'], 1)
            pdf.ln()

        # Output to temp file then read as bytes
        # FPDF 1.7.2 output() returns a string in some versions, or writes to file.
        # Safest way for Streamlit is to write to a temppath and read bytes.
        
        # Note: Using latin-1 encoding by default in FPDF. 
        # If special chars are needed, unicode font setup is required. 
        # For this demo, assuming standard english.
        
        return pdf.output(dest='S').encode('latin-1')
