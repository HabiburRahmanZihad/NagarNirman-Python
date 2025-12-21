import streamlit as st
import pandas as pd
import base64
from datetime import datetime
from utils.data_manager import DataManager
from utils.auth_manager import AuthManager
from utils.ui_manager import UIManager

def show_admin_page():
    """Authority Dashboard with WOW Version analytics and management tools."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    if not AuthManager.is_admin():
        st.error("Access Denied. Admin privileges required.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Hero Title
    st.markdown("""
        <div style="margin-bottom: var(--space-8);">
            <h1 style="margin:0; font-size:2.8rem;">🛡️ Authority Dashboard</h1>
            <p style="font-size:1.1rem; opacity:0.8; letter-spacing:0.02em;">Administrative control center for urban infrastructure management.</p>
        </div>
    """, unsafe_allow_html=True)
    
    reports = DataManager.get_all_reports()
    
    if not reports:
        st.info("No reports found in the system.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # BOSS Metrics Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    total = len(reports)
    resolved = sum(1 for r in reports if r["status"] == "Resolved")
    pending = total - resolved
    efficiency = (resolved/total*100) if total > 0 else 0
    
    with m_col1:
        UIManager.render_custom_metric("Total Reports", total, "📊")
    with m_col2:
        UIManager.render_custom_metric("Resolved Cases", resolved, "✅")
    with m_col3:
        UIManager.render_custom_metric("Pending Issues", pending, "⏳")
    with m_col4:
        UIManager.render_custom_metric("Efficiency", f"{efficiency:.1f}%", "📈")

    st.markdown('<div style="margin-top: var(--space-10);"></div>', unsafe_allow_html=True)

    # Management & Export
    col_list, col_act = st.columns([7, 3])
    
    with col_list:
        st.markdown("### 🛠️ Active Case Management")
        df = pd.DataFrame(reports)
        cols = ['id', 'title', 'category', 'status', 'date']
        # The dataframe container is styled via global CSS
        st.dataframe(df[cols], use_container_width=True, hide_index=True)
        
        # BOSS Export Section
        st.markdown('<div style="margin-top: var(--space-6);"></div>', unsafe_allow_html=True)
        
        export_content = """
            <div style="display: flex; align-items: center; gap: var(--space-4); margin-bottom: var(--space-4);">
                <div style="font-size: 2rem;">📋</div>
                <div>
                    <strong style="font-size: 1.1rem; display: block; color: var(--color-primary);">System-Wide Intelligence Report</strong>
                    <span style="font-size: 0.85rem; opacity: 0.8;">Generate a high-fidelity PDF containing all active and resolved infrastructure reports.</span>
                </div>
            </div>
        """
        UIManager.render_wow_card(export_content)
        
        # Lazy generation: generate PDF only when admin clicks the button.
        # Add a small spacer so the button isn't flush against the card above.
        st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
        if st.button("📥 Generate & Download System Report (PDF)", use_container_width=True, type="primary", key="admin_generate_download"):
            pdf_data = DataManager.generate_reports_pdf(reports)
            if pdf_data:
                try:
                    filename = f"NagarNirman_Report_{datetime.now().strftime('%Y%m%d')}.pdf"
                    # Provide a direct download button (reliable) and a backup anchor link
                    st.download_button(
                        label="📥 Download System Report (PDF)",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True,
                        key="admin_download_btn_generated"
                    )

                    # Base64 link as a visible fallback (some browsers/clients may prefer it)
                    try:
                        b64 = base64.b64encode(pdf_data).decode('ascii')
                        dl_html = f'<div style="margin-top:8px"><a href="data:application/pdf;base64,{b64}" download="{filename}">Click here if download does not start</a></div>'
                        st.markdown(dl_html, unsafe_allow_html=True)
                    except Exception:
                        # If base64 encoding fails for very large files, skip the anchor fallback.
                        pass

                    st.success("PDF ready — use the button above to download.")
                except Exception as e:
                    st.error(f"Failed to prepare download: {e}")
            else:
                st.info("Preparing PDF engine... If this persists, please contact system admin.")
        
    with col_act:
        st.markdown("### 🔄 Update Status")
        status_form_html = """
            <div style="padding: var(--space-1); line-height:1.6; opacity:0.9; margin-bottom:var(--space-4);">
                Select a report ID to modify its current system status. Changes are reflected immediately across the platform.
            </div>
        """
        UIManager.render_wow_card(status_form_html)
        
        report_ids = [str(r['id']) for r in reports]
        selected_id = st.selectbox("Assign ID", report_ids)
        new_status = st.selectbox("New Status", ["Pending", "In Progress", "Resolved"])
        
        if st.button("💾 Apply Update", use_container_width=True, type="primary"):
            if DataManager.update_status(int(selected_id), new_status):
                st.success(f"Report #{selected_id} updated.")
                st.rerun()

    # Detailed Audit Feed
    st.markdown('<div style="margin-top: var(--space-12);"></div>', unsafe_allow_html=True)
    st.markdown("## 📄 Detailed Audit Records")
    for report in reversed(reports):
        with st.expander(f"Audit #{report['id']} - {report['title']} ({report['status']})"):
            UIManager.render_report_card(report)
    
    st.markdown('</div>', unsafe_allow_html=True) # End fade-in
