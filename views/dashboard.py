import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.ui_manager import UIManager

def show_dashboard():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Hero Title
    st.markdown("""
        <div style="margin-bottom: var(--space-6);">
            <h1 style="margin:0; font-size:2.8rem;">🌆 City Overview</h1>
            <p style="font-size:1.1rem; opacity:0.8; letter-spacing:0.02em;">Real-time pulse of infrastructure and urban reports.</p>
        </div>
    """, unsafe_allow_html=True)
    
    reports = DataManager.get_all_reports()
    
    # Validation for Empty Data
    if not reports:
        st.info("No data available yet.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # BOSS Metrics Row
    m_col1, m_col2, m_col3 = st.columns(3)
    total = len(reports)
    resolved = sum(1 for r in reports if r["status"] == "Resolved")
    pending = total - resolved
    
    with m_col1:
        UIManager.render_custom_metric("Total Reports", total, "🌍")
    with m_col2:
        UIManager.render_custom_metric("Resolved Cases", resolved, "✅")
    with m_col3:
        UIManager.render_custom_metric("Active Issues", pending, "⏳")

    st.markdown('<div style="margin-top: var(--space-8);"></div>', unsafe_allow_html=True)

    # Main Grid Layout for Map and Insights
    col_map, col_stat = st.columns([7.5, 2.5])
    
    with col_map:
        st.markdown("### 📍 Issue Hotspots")
        df = pd.DataFrame(reports)
        # The map is styled automatically via CSS targeting the iframe container
        st.map(df, zoom=11, size=30, color="#FF4B4B")
        
    with col_stat:
        st.markdown("### 📊 Insights")
        resolved_rate = (resolved/total)*100 if total > 0 else 0
        
        insight_html = f"""
            <div style="padding: var(--space-2);">
                <div style="font-size: 0.9rem; opacity:0.7; margin-bottom:var(--space-2);">RESOLUTION RATE</div>
                <div style="font-size: 2.5rem; font-weight:800; color:var(--color-primary);">{resolved_rate:.1f}%</div>
                <div style="margin-top: var(--space-4); font-size:0.85rem; line-height:1.4;">
                    Our commitment to a better city is reflected in every resolved case.
                </div>
            </div>
        """
        UIManager.render_wow_card(insight_html)
        st.progress(resolved_rate/100)

    # Recent Reports Feed
    st.markdown('<div style="margin-top: var(--space-10);"></div>', unsafe_allow_html=True)
    st.markdown("## 📝 Global Issue Feed")
    UIManager.render_report_cards_grid(list(reversed(reports)), columns=4)
    
    st.markdown('</div>', unsafe_allow_html=True) # End fade-in
