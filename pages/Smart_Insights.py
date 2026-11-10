import streamlit as st
import pandas as pd  # [web:117][web:120]
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import theme

theme.apply_modern_theme()

st.set_page_config(
    page_title="Smart Insights – DataVisionX",
    page_icon="💡",
    layout="wide",
)

# ---------- STYLES ----------

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
        .pill-badge {
            display: inline-block;
            padding: 0.1rem 0.6rem;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 600;
            margin-right: 0.4rem;
            color: #05061a;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER ----------

st.markdown('<div class="section-title">Smart Insights</div>', unsafe_allow_html=True)
st.write("Rule‑based recommendations on data quality, structure, and potential issues in your dataset.")

# ---------- CHECK DATA ----------

if "df" not in st.session_state:
    st.warning("No dataset found. Please upload a file in 'Upload & Overview' first.")
    st.stop()

df: pd.DataFrame = st.session_state["df"]

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = df.select_dtypes(exclude=["int64", "float64"]).columns.tolist()

# ---------- RULE FUNCTIONS ----------

def generate_missing_value_insights(data: pd.DataFrame):
    insights = []
    missing_pct = data.isna().mean().sort_values(ascending=False) * 100
    for col, pct in missing_pct.items():
        if pct == 0:
            continue
        if pct > 40:
            level = "Critical"
            msg = f"{col} has very high missing values ({pct:.1f}%). Consider dropping this column or using advanced imputation."
        elif pct > 15:
            level = "Warning"
            msg = f"{col} has moderate missing values ({pct:.1f}%). Filling with median/most frequent or adding an 'Unknown' category can help."
        else:
            level = "Info"
            msg = f"{col} has some missing values ({pct:.1f}%). Simple imputation (mean/median/mode) should be enough."
        insights.append((level, "Missing values", msg))
    return insights  # [web:117][web:120]


def generate_cardinality_insights(data: pd.DataFrame, cat_cols):
    insights = []
    for col in cat_cols:
        nunique = data[col].nunique(dropna=True)
        if nunique == 0:
            continue
        if nunique > 50:
            level = "Warning"
            msg = f"{col} has very high cardinality ({nunique} unique values). Consider grouping or encoding carefully."
            insights.append((level, "High cardinality", msg))
        elif nunique == 1:
            level = "Info"
            msg = f"{col} has only one unique value. It may not contribute useful information."
            insights.append((level, "Low variance", msg))
    return insights


def generate_outlier_insights(data: pd.DataFrame, num_cols):
    insights = []
    for col in num_cols:
        series = data[col].dropna()
        if series.empty:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers_pct = ((series < lower) | (series > upper)).mean() * 100
        if outliers_pct > 20:
            level = "Warning"
            msg = f"{col} shows many outliers (~{outliers_pct:.1f}% of values). Check for data entry errors or consider robust scaling/winsorization."
            insights.append((level, "Outliers", msg))
    return insights  # [web:117][web:124]


def generate_correlation_insights(data: pd.DataFrame, num_cols):
    insights = []
    if len(num_cols) < 2:
        return insights
    corr = data[num_cols].corr().abs()  # [web:121][web:125]
    # zero diagonal
    corr.values[range(corr.shape[0]), range(corr.shape[0])] = 0
    pairs = (
        corr.where(corr > 0.8)
        .stack()
        .reset_index()
        .rename(columns={"level_0": "col1", "level_1": "col2", 0: "corr"})
    )
    for _, row in pairs.iterrows():
        level = "Info"
        msg = f"{row['col1']} and {row['col2']} are highly correlated (corr ≈ {row['corr']:.2f}). One of them might be redundant."
        insights.append((level, "High correlation", msg))
    return insights  # [web:115][web:118]


def generate_duplicate_insights(data: pd.DataFrame):
    insights = []
    dup_pct = data.duplicated().mean() * 100
    if dup_pct == 0:
        return insights
    if dup_pct > 10:
        level = "Warning"
        msg = f"{dup_pct:.1f}% of rows are duplicates. Consider deduplicating or investigating ingestion issues."
    else:
        level = "Info"
        msg = f"{dup_pct:.1f}% duplicate rows detected. Review if duplicates are expected."
    insights.append((level, "Duplicates", msg))
    return insights


# ---------- AGGREGATE & RENDER ----------
all_insights = []
all_insights.extend(generate_missing_value_insights(df))
all_insights.extend(generate_cardinality_insights(df, categorical_cols))
all_insights.extend(generate_outlier_insights(df, numeric_cols))
all_insights.extend(generate_correlation_insights(df, numeric_cols))
all_insights.extend(generate_duplicate_insights(df))

if not all_insights:
    st.success("No notable issues detected in the current dataset.")
else:
    ins_df = pd.DataFrame(all_insights, columns=["Level", "Issue", "Message"])
    # Present findings grouped by severity
    for lvl in ["Critical", "Warning", "Info"]:
        subset = ins_df[ins_df["Level"] == lvl]
        if not subset.empty:
            st.subheader(f"{lvl} findings")
            for _, r in subset.iterrows():
                st.write(f"- **{r['Issue']}**: {r['Message']}")

    # Provide a downloadable plain-text report of insights
    report_lines = []
    for _, r in ins_df.iterrows():
        report_lines.append(f"[{r['Level']}] {r['Issue']}: {r['Message']}")
    report_text = "\n".join(report_lines)
    st.download_button(
        label="⬇ Download Insights",
        data=report_text,
        file_name="datavisionx_insights.txt",
        mime="text/plain",
    )