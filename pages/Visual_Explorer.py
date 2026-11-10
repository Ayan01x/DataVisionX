import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from typing import Optional
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import theme

theme.apply_modern_theme()

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Visual Explorer – DataVisionX", page_icon="🔮", layout="wide")

# Initialize theme defaults
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"
if "primary_color" not in st.session_state:
    st.session_state["primary_color"] = "#D946EF"  # Neon Fuchsia
if "secondary_color" not in st.session_state:
    st.session_state["secondary_color"] = "#8B5CF6" # Neon Purple

# --- 2. MODERN STYLING (CSS) ---
bg_color = "#0B0C15"
card_bg = "rgba(23, 25, 41, 0.7)"
font_color = "#E2E8F0"
grid_color = "#2D3748"

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {bg_color};
        }}
        .section-title {{
            font-size: 28px;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #D946EF, #8B5CF6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }}
        .card {{
            background: {card_bg};
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 24px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
        }}
        /* Improve Selectbox styling */
        div[data-baseweb="select"] > div {{
            background-color: #1E293B;
            border-color: #475569;
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Visual Explorer </div>', unsafe_allow_html=True)

# --- 3. DATA LOADING ---
if "df" not in st.session_state:
    st.warning("⚠️ No dataset found. Please upload a file in 'Upload & Overview' first.")
    st.stop()
else:
    df: pd.DataFrame = st.session_state["df"]

numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
categorical_cols = [c for c in df.columns if c not in numeric_cols]
filtered_df = df.copy()

# --- 4. PLOTLY THEME HELPERS ---
def apply_modern_layout(fig):
    """Applies the DataVisionX Neon/Dark theme to Plotly figures."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=font_color),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(gridcolor=grid_color, showgrid=True),
        yaxis=dict(gridcolor=grid_color, showgrid=True),
    )
    return fig

# --- 5. CHART FUNCTIONS ---

def make_3d_scatter(df_, x, y, z, color):
    if not z or z == "(none)":
        # Fallback to glamorous 2D
        fig = px.scatter(
            df_, x=x, y=y, color=color if color != "(none)" else None,
            color_discrete_sequence=[st.session_state["primary_color"]],
            render_mode='webgl'
        )
        fig.update_traces(marker=dict(size=10, line=dict(width=1, color="white"), opacity=0.8))
    else:
        fig = px.scatter_3d(
            df_, x=x, y=y, z=z, color=color if color != "(none)" else None,
            color_discrete_sequence=[st.session_state["primary_color"]]
        )
        fig.update_traces(marker=dict(size=5, opacity=0.8))
    return apply_modern_layout(fig)

def make_3d_line(df_, x, y, z, color):
    if not z or z == "(none)":
        fig = px.line(
            df_, x=x, y=y, color=color if color != "(none)" else None,
            markers=True,
            color_discrete_sequence=[st.session_state["primary_color"]]
        )
        fig.update_traces(line=dict(width=3))
    else:
        fig = px.line_3d(
            df_, x=x, y=y, z=z, color=color if color != "(none)" else None,
            color_discrete_sequence=[st.session_state["primary_color"]]
        )
        fig.update_traces(line=dict(width=4))
    return apply_modern_layout(fig)

def make_neon_bar(df_, x, y, color):
    if y and pd.api.types.is_numeric_dtype(df_[y]):
        grouped = df_.groupby(x)[y].mean().reset_index()
        fig = px.bar(grouped, x=x, y=y, color=y, color_continuous_scale="Bluered_r")
    else:
        counts = df_[x].value_counts().reset_index()
        counts.columns = [x, 'count']
        fig = px.bar(counts, x=x, y='count', color='count', color_continuous_scale="Bluered_r")
    return apply_modern_layout(fig)

def make_simple_bar(df_, x, y, color):
    """Cleaner, solid color bar chart."""
    if y and pd.api.types.is_numeric_dtype(df_[y]):
        grouped = df_.groupby(x)[y].mean().reset_index()
        # If user picked a color column, use it, otherwise use Primary Color
        c = color if color != "(none)" else None
        # If color is None, use discrete sequence
        fig = px.bar(
            grouped, x=x, y=y, color=c,
            color_discrete_sequence=[st.session_state["primary_color"]]
        )
    else:
        counts = df_[x].value_counts().reset_index()
        counts.columns = [x, 'count']
        c = color if color != "(none)" else None
        fig = px.bar(
            counts, x=x, y='count', color=c,
            color_discrete_sequence=[st.session_state["primary_color"]]
        )
    fig.update_traces(marker_line_width=0)
    return apply_modern_layout(fig)

def make_animated_histogram(df_, x, color, anim_frame):
    """Histogram that animates over a time/category variable."""
    if anim_frame == "(none)":
        # Fallback to standard histogram if no animation frame selected
        fig = px.histogram(
            df_, x=x, color=color if color != "(none)" else None,
            color_discrete_sequence=[st.session_state["primary_color"]],
            nbins=30
        )
    else:
        # We need to sort by animation frame for smooth playback
        df_sorted = df_.sort_values(by=anim_frame)
        fig = px.histogram(
            df_sorted, x=x, 
            animation_frame=anim_frame,
            color=color if color != "(none)" else None,
            color_discrete_sequence=[st.session_state["primary_color"]],
            nbins=30
        )
        # Slow down animation slightly for better visuals
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 800

    fig.update_traces(marker_line_width=0)
    return apply_modern_layout(fig)

def make_area_fill(df_, x, y):
    fig = px.area(df_, x=x, y=y, color_discrete_sequence=[st.session_state["primary_color"]])
    fig.update_traces(line=dict(width=0))
    return apply_modern_layout(fig)

# --- 6. RENDER LAYOUT ---

st.markdown('<div class="card">', unsafe_allow_html=True)
chart_placeholder = st.empty()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title" style="font-size:20px;">Configuration</div>', unsafe_allow_html=True)

# 5 Columns for controls
c1, c2, c3, c4, c5 = st.columns([1.2, 1, 1, 1, 1])

with c1:
    chart_type = st.selectbox(
        "Chart Style",
        ["Scatter", "Line", "Neon Bar", "Simple Bar", "Histogram", "Area Fill", "Correlation Matrix"]
    )

with c2:
    x_col = st.selectbox("X Axis (Base)", options=df.columns)

with c3:
    y_options = [c for c in df.columns if c != x_col]
    # Y is needed for almost everything except Histogram
    if chart_type == "Histogram":
         y_col = "(none)"
         st.markdown("<div style='margin-top: 32px; color: #555;'>Y calc. auto</div>", unsafe_allow_html=True)
    else:
         y_col = st.selectbox("Y Axis (Height)", options=["(none)"] + y_options, index=0)

with c4:
    # Z-Axis logic (only for 3D)
    if "3D" in chart_type:
        z_options = [c for c in numeric_cols if c not in [x_col, y_col]]
        z_col = st.selectbox("Z Axis (Depth)", options=["(none)"] + z_options)
    # Animation Frame logic (only for Animated Histogram)
    elif chart_type == "Histogram":
        anim_options = [c for c in df.columns if c != x_col]
        anim_col = st.selectbox("Animation Frame", options=["(none)"] + anim_options)
        z_col = "(none)" # unused
    else:
        z_col = "(none)"
        st.markdown("<div style='margin-top: 32px; color: #555;'>Not applicable</div>", unsafe_allow_html=True)

with c5:
    color_options = [c for c in df.columns if c not in [x_col, y_col]]
    color_col = st.selectbox("Color Group", options=["(none)"] + color_options)

# Filter Logic (Range slider)
with st.expander("Filter Data"):
    filter_col = st.selectbox("Filter Column", options=["(none)"] + numeric_cols)
    if filter_col != "(none)":
        min_v, max_v = float(df[filter_col].min()), float(df[filter_col].max())
        rng = st.slider(f"Range: {filter_col}", min_v, max_v, (min_v, max_v))
        filtered_df = filtered_df[filtered_df[filter_col].between(rng[0], rng[1])]

# --- 7. CHART GENERATION ---
if filtered_df.empty:
    st.error("No data matches the current filters.")
else:
    try:
        fig = go.Figure()
        
        if chart_type == "Scatter":
            if y_col == "(none)": st.warning("Please select a Y axis.")
            else: fig = make_3d_scatter(filtered_df, x_col, y_col, z_col, color_col)

        elif chart_type == "Line":
            if y_col == "(none)": st.warning("Please select a Y axis.")
            else: fig = make_3d_line(filtered_df, x_col, y_col, z_col, color_col)

        elif chart_type == "Neon Bar":
             fig = make_neon_bar(filtered_df, x_col, y_col, color_col)
        
        elif chart_type == "Simple Bar":
             fig = make_simple_bar(filtered_df, x_col, y_col, color_col)

        elif chart_type == "Histogram":
             # anim_col is defined in the controls block c4
             fig = make_animated_histogram(filtered_df, x_col, color_col, anim_col)

        elif chart_type == "Area Fill":
            if y_col == "(none)" or not pd.api.types.is_numeric_dtype(filtered_df[y_col]):
                st.warning("Area chart requires numeric Y axis.")
            else: fig = make_area_fill(filtered_df, x_col, y_col)

        elif chart_type == "Correlation Matrix":
            corr = filtered_df[numeric_cols].corr()
            fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
            apply_modern_layout(fig)

        with chart_placeholder:
            st.plotly_chart(fig, use_container_width=True, theme=None)

    except Exception as e:
        st.error(f"Could not render chart: {e}")