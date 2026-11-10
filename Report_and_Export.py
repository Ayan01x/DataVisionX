import streamlit as st
import pandas as pd
import io  # [web:73][web:87]
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import theme

theme.apply_modern_theme()

st.set_page_config(page_title="Report & Export – DataVisionX", page_icon="📑", layout="wide")

st.markdown(
    """
    <style>
        .main {
            background-color: #05061a;
            color: #f5f5ff;
        }
        .section-title {
            font-size: 24px;
            font-weight: 700;
            margin-top: 0.5rem;
            color: #ffffff;
        }
        .card {
            padding: 1.0rem 1.2rem;
            border-radius: 0.8rem;
            background: #11122e;
            border: 1px solid #2a2b5f;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Report & Export</div>', unsafe_allow_html=True)
st.write("Download a summary report and the cleaned dataset for further use.")

if "df" not in st.session_state:
    st.warning("No dataset found. Please upload a file in 'Upload & Overview' first.")
    st.stop()

df: pd.DataFrame = st.session_state["df"].copy()

st.subheader("Cleaned dataset preview")
clean_df = df.dropna(how="all")  # simple cleaning rule
st.dataframe(clean_df.head(), use_container_width=True)  # [web:73]

st.write("")
st.markdown("### Download cleaned CSV")

csv_buffer = io.StringIO()
clean_df.to_csv(csv_buffer, index=False)
csv_bytes = csv_buffer.getvalue().encode("utf-8")

st.download_button(
    label="⬇ Download Cleaned CSV",
    data=csv_bytes,
    file_name="datavisionx_cleaned.csv",
    mime="text/csv",
)

st.write("")
st.markdown("### Generate HTML summary report")

if st.button("Create HTML Report"):
    with st.spinner("Generating summary report..."):
        numeric_cols = clean_df.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = clean_df.select_dtypes(exclude=["number"]).columns.tolist()

        lines = []
        lines.append("DataVisionX Summary Report")
        lines.append("=" * 30)
        lines.append(f"Rows: {clean_df.shape[0]}, Columns: {clean_df.shape[1]}")
        lines.append("")
        lines.append("Column types:")
        lines.append(clean_df.dtypes.astype(str).to_string())
        lines.append("")
        lines.append("Missing values (%) per column:")
        mv = (clean_df.isna().mean() * 100).round(2).sort_values(ascending=False)
        lines.append(mv.to_string())

        if numeric_cols:
            lines.append("")
            lines.append("Numeric summary (describe):")
            lines.append(clean_df[numeric_cols].describe().to_string())

        if categorical_cols:
            lines.append("")
            lines.append("Categorical columns (unique counts):")
            lines.append(clean_df[categorical_cols].nunique().to_string())

        report_text = "\n\n".join(lines)

        st.text_area("Report preview", value=report_text, height=400)

        st.download_button(
            label="⬇ Download Report (.txt)",
            data=report_text,
            file_name="datavisionx_report.txt",
            mime="text/plain",
        )