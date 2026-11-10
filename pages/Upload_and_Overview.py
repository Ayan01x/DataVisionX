import streamlit as st
import pandas as pd
import sys
import os

# Allow importing theme.py from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import theme

st.set_page_config(page_title="Upload – DataVisionX", page_icon="📂", layout="wide")
theme.apply_modern_theme()

st.markdown('<div class="animate-enter">', unsafe_allow_html=True)
st.markdown('<h1>📂 Upload & Overview</h1>', unsafe_allow_html=True)
st.write("Upload a CSV or Excel file to initialize the DataVisionX engine.")

# Upload Area using standard Streamlit but styled via global CSS
uploaded_file = st.file_uploader(
    "Drag and drop your dataset here",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.session_state["df"] = df

        # --- ANIMATED METRICS ROW ---
        n_rows, n_cols = df.shape
        missing = df.isna().sum().sum()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        
        # Helper to create metric card
        def metric_card(label, value, icon, col):
            col.markdown(f"""
            <div class="modern-card" style="padding: 20px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
                <div style="color: #94A3B8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
                <div style="font-size: 28px; font-weight: 800; color: #F8FAFC;">{value}</div>
            </div>
            """, unsafe_allow_html=True)

        metric_card("Rows", f"{n_rows:,}", "📝", m1)
        metric_card("Columns", f"{n_cols}", "🏗️", m2)
        metric_card("Missing Values", f"{missing}", "🔍", m3)
        metric_card("File Type", uploaded_file.name.split('.')[-1].upper(), "📄", m4)

        # --- PREVIEW SECTION ---
        st.markdown("<br><h3>📋 Data Snapshot</h3>", unsafe_allow_html=True)
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- DATA TYPES SECTION ---
        with st.expander("View Column Data Types"):
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            dtype_df = df.dtypes.astype(str).reset_index()
            dtype_df.columns = ["Column", "Type"]
            st.dataframe(dtype_df.T, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    # Empty State (Modern)
    st.markdown("""
    <div class="modern-card" style="text-align: center; margin-top: 50px; padding: 60px;">
        <div style="font-size: 60px; margin-bottom: 20px; opacity: 0.5;">📤</div>
        <h3 style="color: #94A3B8;">Awaiting Dataset</h3>
        <p>Please upload a file above to begin analysis.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)