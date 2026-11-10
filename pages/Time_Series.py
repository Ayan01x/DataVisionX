import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Allow importing theme from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import theme

# Apply global theme
theme.apply_modern_theme()

# Altair for interactive charts (fallback to Matplotlib if unavailable)
try:
    import altair as alt
except Exception:
    alt = None

# Page config
st.set_page_config(
    page_title="Time Series – DataVisionX",
    page_icon="⏱",
    layout="wide",
)

# Title / description
st.markdown(
    """
    <h2 style="margin-bottom:0;">Time Series Explorer</h2>
    <p style="color:#94A3B8; margin-top:4px;">
        Analyze trends, seasonality, and moving averages for date‑based data.
    </p>
    """,
    unsafe_allow_html=True,
)

# Ensure dataset is available
if "df" not in st.session_state:
    st.warning("No dataset found. Please upload a file in 'Upload & Overview' first.")
    st.stop()

df: pd.DataFrame = st.session_state["df"].copy()

# Show column dtypes for transparency / debugging
st.write("Column types:")
st.dataframe(df.dtypes.to_frame(name="dtype"))

# ---------- DATE DETECTION (SAFE) ----------

# 1. Use existing datetime columns
auto_date_cols = [
    c for c in df.columns
    if pd.api.types.is_datetime64_any_dtype(df[c])
]

# 2. If none, try to parse only object columns as dates
if not auto_date_cols:
    for c in df.columns:
        if df[c].dtype == "object":
            parsed = pd.to_datetime(df[c], errors="coerce")
            if parsed.notna().mean() > 0.8:  # majority valid dates
                df[c] = parsed
                auto_date_cols.append(c)

if not auto_date_cols:
    st.error("No suitable date/time column detected. Please ensure your dataset has a date column.")
    st.stop()

# Let user pick date column
date_col = st.selectbox("Select date column", auto_date_cols)
df = df.sort_values(by=date_col)

# ---------- NUMERIC COLUMN DETECTION ----------

numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

if not numeric_cols:
    st.error("No numeric columns available for time‑series analysis.")
    st.stop()

value_col = st.selectbox("Select value column", numeric_cols)

# Resample frequency and moving average window
freq = st.selectbox(
    "Resample frequency",
    options=["D", "W", "M"],
    format_func=lambda x: {"D": "Daily", "W": "Weekly", "M": "Monthly"}[x],
)

window = st.slider("Moving average window (periods)", 1, 60, 7)

# Build a time-series friendly DataFrame
df_ts = df[[date_col, value_col]].dropna()
df_ts = df_ts.set_index(date_col).resample(freq).mean()

# ---------- MAIN TREND CHART (ALTair if available) ----------

if alt is not None:
    try:
        df_plot = df_ts.reset_index().rename(columns={date_col: "date"})
        df_plot["rolling"] = df_plot[value_col].rolling(window).mean()

        hover = alt.selection_single(on="mouseover", empty="none", nearest=True)

        chart_actual = (
            alt.Chart(df_plot)
            .mark_line(color="#4f46e5", size=2.5, point=alt.OverlayMarkDef(filled=True, size=50))
            .encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y(f"{value_col}:Q", title=value_col),
                tooltip=["date:T", f"{value_col}:Q"],
                opacity=alt.condition(hover, alt.value(1), alt.value(0.7)),
            )
            .add_selection(hover)
        )

        chart_ma = (
            alt.Chart(df_plot)
            .mark_line(color="#ff4b9f", size=2.5, strokeDash=[5, 5])
            .encode(
                x="date:T",
                y=alt.Y("rolling:Q", title=f"Rolling mean ({window})"),
                tooltip=["date:T", alt.Tooltip("rolling:Q", format=".2f")],
                opacity=alt.condition(hover, alt.value(1), alt.value(0.5)),
            )
            .add_selection(hover)
        )

        combined = (
            alt.layer(chart_actual, chart_ma)
            .resolve_scale(y="shared")
            .properties(height=420)
        )

        brush = alt.selection(type="interval", encodings=["x"])
        upper = combined.add_selection(brush).properties(height=120)
        lower = combined.encode(
            opacity=alt.condition(brush, alt.value(1), alt.value(0.3))
        ).properties(height=360)

        st.altair_chart(alt.vconcat(lower, upper), use_container_width=True)
    except Exception:
        alt = None

# ---------- MATPLOTLIB FALLBACK ----------

if alt is None:
    sns.set_style("darkgrid")
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("#05061a")
    ax.set_facecolor("#05061a")

    ax.plot(df_ts.index, df_ts[value_col], label="Actual", color="#4f46e5")
    ax.plot(
        df_ts.index,
        df_ts[value_col].rolling(window).mean(),
        label=f"Rolling mean ({window})",
        color="#ff4b9f",
    )

    ax.set_title(f"{value_col} over time ({freq})")
    ax.set_xlabel("Date")
    ax.set_ylabel(value_col)
    ax.legend()

    st.pyplot(fig)

st.write("")

# ---------- SEASONALITY VIEW (REDESIGNED) ----------

st.markdown(
    """
    <div style="margin-top:32px; margin-bottom:8px;">
        <h3 style="margin-bottom:4px;">Seasonality view</h3>
        <p style="color:#94A3B8; font-size:0.9rem;">
            Compare the average value by month or day of week to spot recurring patterns.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

group_choice = st.selectbox(
    "Group by",
    ["Month", "Day of week"],
)

if group_choice == "Month":
    temp = df_ts.copy()
    temp["month"] = temp.index.month
    seasonal = temp.groupby("month")[value_col].mean()
    x_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    idx = range(1, 13)
else:
    temp = df_ts.copy()
    temp["dow"] = temp.index.dayofweek
    seasonal = temp.groupby("dow")[value_col].mean()
    x_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    idx = range(0, 7)

# Nice looking bar chart
fig2, ax2 = plt.subplots(figsize=(8.5, 4))
fig2.patch.set_facecolor("#05061a")
ax2.set_facecolor("#05061a")

# Use a softer color and slimmer bars
bars = ax2.bar(
    list(idx),
    seasonal.values,
    color="#22c55e",
    edgecolor="#16a34a",
    linewidth=1.2,
    alpha=0.9,
)

ax2.set_xticks(list(idx))
ax2.set_xticklabels(x_labels, fontsize=10, color="#E5E7EB")
ax2.set_ylabel(value_col, color="#E5E7EB")
ax2.set_title(f"Average {value_col} by {group_choice.lower()}", color="#E5E7EB", pad=12)

# Light horizontal grid for readability
ax2.grid(axis="y", alpha=0.25, color="#9CA3AF")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_color("#4B5563")
ax2.spines["bottom"].set_color("#4B5563")
ax2.tick_params(colors="#E5E7EB")

# Add value labels on top of each bar
for rect, val in zip(bars, seasonal.values):
    height = rect.get_height()
    ax2.text(
        rect.get_x() + rect.get_width() / 2,
        height + (seasonal.values.max() * 0.01),
        f"{val:.1f}",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#E5E7EB",
    )

st.pyplot(fig2)