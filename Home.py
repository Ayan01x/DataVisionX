import streamlit as st
import theme  # Import your new global theme
import urllib.parse

# 1. PAGE CONFIG
st.set_page_config(
    page_title="DataVisionX – AI Analytics",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. APPLY THEME
theme.apply_modern_theme()

# ---------------------------------------------------------
# CUSTOM CSS (Navbar, Cards, Workflow)
# ---------------------------------------------------------
st.markdown("""
<style>
/* --- NAVBAR (Fixed & Responsive) --- */
.dvx-nav-container {
    display: flex;
    justify_content: center;
    width: 100%;
    margin-bottom: 20px;
}

.dvx-nav {
    display: flex;
    gap: 20px;
    align-items: center;
    padding: 12px 30px;
    border-radius: 50px;
    background: rgba(15, 23, 42, 0.6); /* More transparent */
    backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid rgba(139,92,246,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.dvx-nav:hover {
    border-color: rgba(139,92,246,0.4);
    background: rgba(15, 23, 42, 0.8);
}

.dvx-nav a {
    color: #cbd5e1;
    text-decoration: none;
    font-weight: 500;
    font-size: 15px;
    padding: 8px 16px;
    border-radius: 20px;
    transition: all 0.2s ease;
    position: relative;
}

.dvx-nav a:hover {
    color: white;
    background: rgba(255,255,255,0.1);
}

/* Highlight 'Contact' as a primary button style */
.dvx-nav a[href="#contact"] {
    background: linear-gradient(90deg, #8B5CF6, #D946EF);
    color: white;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(217, 70, 239, 0.3);
}
.dvx-nav a[href="#contact"]:hover {
    box-shadow: 0 6px 16px rgba(217, 70, 239, 0.5);
    transform: translateY(-1px);
}


/* --- POWERFUL FEATURES (High Intensity Hover) --- */
.modern-card {
    background: #1e293b; /* Dark card bg */
    padding: 2rem;
    border-radius: 1rem;
    border: 1px solid rgba(255,255,255,0.05);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Bouncy transition */
    height: 100%;
}

.modern-card:hover {
    transform: translateY(-12px) scale(1.02); /* Lifts up higher */
    background: linear-gradient(145deg, #1e293b, #252b42);
    border-color: #D946EF; /* Pink border on hover */
    box-shadow: 0 20px 50px rgba(217, 70, 239, 0.2); /* Strong glow */
}

/* --- WORKFLOW CARDS (Restored & Improved) --- */
.step-card {
    background: #1e293b;
    border-radius: 1rem;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.05);
    height: 100%;
    position: relative;
    overflow: hidden;
}

.step-card:hover {
    transform: translateY(-8px);
    border-color: #8B5CF6; /* Purple border */
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.15);
}

.step-number {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8B5CF6, #D946EF);
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    line-height: 50px;
    margin: 0 auto 1.5rem auto;
    box-shadow: 0 4px 15px rgba(217, 70, 239, 0.4);
}

/* UTILS */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    margin: 4rem 0;
}
</style>

<!-- Navigation Bar (Centered Container) -->
<div class="dvx-nav-container">
    <div class="dvx-nav">
      <a href="#about">About</a>
      <a href="#workflow">Workflow</a>
      <a href="#review">Feedback</a>
      <a href="#contact">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. HERO SECTION
st.markdown("""
<div class="animate-enter" style="text-align: center; margin-top: 20px; margin-bottom: 80px;">
    <div style="
        display: inline-block;
        padding: 8px 20px;
        background: rgba(139, 92, 246, 0.15);
        border-radius: 30px;
        color: #D946EF;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 24px;
        border: 1px solid rgba(139, 92, 246, 0.3);">
        ✨ The Future of Data Analysis
    </div>
    <h1 style="font-size: 72px; margin-bottom: 15px; line-height: 1.1; font-weight: 800;">
        Unlock Insights with <br>
        <span class="gradient-text" style="background: linear-gradient(to right, #8B5CF6, #D946EF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">DataVisionX</span>
    </h1>
    <p style="color: #94A3B8; font-size: 22px; max-width: 700px; margin: 0 auto 40px auto; line-height: 1.6;">
        Automated EDA, advanced interactive visualizations, and ML-ready reports in seconds. 
        Zero coding required.
    </p>
</div>
""", unsafe_allow_html=True)

# 4. START BUTTON (Centered)
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("🚀 Get Started Now", use_container_width=True):
        st.switch_page("pages/Upload_and_Overview.py")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 5. FEATURES GRID (With Intense Hover)
st.markdown('<h2 style="text-align:center; margin-bottom: 50px; font-size: 2.5rem;">Powerful Features</h2>', unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.markdown("""
    <div class="modern-card">
        <div style="font-size: 48px; margin-bottom: 20px;">📊</div>
        <h3 style="font-size: 24px; font-weight: 700; margin-bottom: 10px;">Interactive Viz</h3>
        <p style="color: #94A3B8; font-size: 16px; line-height: 1.6;">
            Ditch static charts. Rotate 3D plots, zoom into time series, and explore data with neon-styled aesthetics.
        </p>
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    st.markdown("""
    <div class="modern-card">
        <div style="font-size: 48px; margin-bottom: 20px;">⚡</div>
        <h3 style="font-size: 24px; font-weight: 700; margin-bottom: 10px;">Automated EDA</h3>
        <p style="color: #94A3B8; font-size: 16px; line-height: 1.6;">
            Upload your file and get instant quality checks, missing value detection, and statistical summaries.
        </p>
    </div>
    """, unsafe_allow_html=True)

with row1_col3:
    st.markdown("""
    <div class="modern-card">
        <div style="font-size: 48px; margin-bottom: 20px;">📑</div>
        <h3 style="font-size: 24px; font-weight: 700; margin-bottom: 10px;">Smart Reports</h3>
        <p style="color: #94A3B8; font-size: 16px; line-height: 1.6;">
            Generate comprehensive HTML/PDF summaries and export cleaned datasets with a single click.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 6. HOW IT WORKS (Restored "Previous" Card Style)
st.markdown('<div id="workflow"></div>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center; margin-bottom: 50px; font-size: 2.5rem;">Workflow</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# Defined steps data
steps_data = [
    (1, "📂", "Upload", "Drag & Drop CSV/Excel"),
    (2, "⚙️", "Process", "Auto-clean & Analyze"),
    (3, "📈", "Visualize", "Explore Patterns"),
    (4, "💾", "Export", "Download Reports"),
]

# Iterate and create cards
for i, (num, icon, title, text) in enumerate(steps_data):
    col = [col1, col2, col3, col4][i]
    with col:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{num}</div>
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icon}</div>
            <h4 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;">{title}</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">{text}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 7. ABOUT (Preserved)
st.markdown('<div id="about"></div>', unsafe_allow_html=True)
st.markdown("## About DataVisionX")
st.markdown("""
<div style="color:#94A3B8; margin-bottom: 20px; font-size: 1.1rem;">
DataVisionX cleans and transforms raw datasets into structured, analysis-ready formats.
</div>
<ul style="color:#94A3B8; line-height:1.8; font-size: 1rem;">
<li>🚀 <strong>Smart Preprocessing</strong> — Handles missing values, inconsistencies, and formatting.</li>
<li>🔍 <strong>EDA-Optimized</strong> — Generates quick insights instantly.</li>
<li>🤖 <strong>ML-Ready Outputs</strong> — Encoding, scaling, and outlier fixes included.</li>
<li>⚡ <strong>Automation</strong> — Save hours of manual cleaning.</li>
</ul>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 8. FEEDBACK (Fixed Form Bug)
st.markdown('<div id="review"></div>', unsafe_allow_html=True)
st.markdown("## Leave a Review")

# Wrap in st.form to fix the "submit" bug
with st.form("review_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        email = st.text_input("Email")
    with col2:
        rating = st.selectbox("Rating", ["⭐ Poor", "⭐⭐ Good", "⭐⭐⭐ Average", "⭐⭐⭐⭐ Excellent"])
    
    review_msg = st.text_area("Your Review", height=120)
    
    # Form Submit Button
    submitted = st.form_submit_button("Submit Review")
    
    if submitted:
        # Check if Name, Email, and Review Message are filled (Rating always has a value)
        if name.strip() and email.strip() and review_msg.strip():
            st.success(f"Thank you {name}! ❤️ Your review has been submitted.")
        else:
            st.error("Please fill all fields (Name, Email, and Review).")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 9. CONTACT
st.markdown('<div id="contact"></div>', unsafe_allow_html=True)
st.markdown("## Contact Us")
st.markdown("📧 [ayanbargir6@gmail.com](mailto:ayanbargir6@gmail.com)")

with st.form("contact_form"):
    subject = st.text_input("Subject")
    msg = st.text_area("Message", height=140)
    contact_submitted = st.form_submit_button("✉️ Contact via Email")

    if contact_submitted:
        if subject.strip() and msg.strip():
            mailto = f"mailto:ayanbargir6@gmail.com?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(msg)}"
            st.markdown(f"[Click to send email]({mailto})")
            st.success("Opening email client…")
        else:
            st.error("Please provide both subject and message.")

# FOOTER
st.markdown("""
<div style="text-align: center; margin-top: 80px; color: #475569; font-size: 12px;">
    &copy; 2025 DataVisionX. Built by Ayan | Mofiz | Anurag ❤️
</div>
""", unsafe_allow_html=True)
