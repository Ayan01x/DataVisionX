import streamlit as st


def apply_modern_theme():
    """
    Applies the comprehensive DataVisionX design system:
    - Modern Sidebar with Glassmorphism
    - Global Animations (Fade In, Slide Up)
    - Hover Effects
    - Custom Scrollbars
    """
    
    # Define the CSS
    css = """
    <style>
        /* --- GLOBAL VARIABLES --- */
        :root {
            --primary: #D946EF;
            --secondary: #8B5CF6;
            --bg-dark: #0B0C15;
            --card-bg: rgba(23, 25, 41, 0.75);
            --text-white: #E2E8F0;
            --sidebar-bg: rgba(11, 12, 21, 0.85);
        }

        /* --- PAGE BACKGROUND --- */
        .stApp {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(217, 70, 239, 0.08) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 20%);
        }

        /* --- MODERN SIDEBAR --- */
        section[data-testid="stSidebar"] {
            background-color: var(--sidebar-bg);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
        }
        
        /* Sidebar Nav Items */
        .css-17lntkn, .css-pkbazv { 
            /* This targets Streamlit's nav links (classes vary by version, using generic selector approach below) */
        }
        
        /* Custom Sidebar Link Styling (Attempting to target Streamlit's internal elements) */
        div[data-testid="stSidebarNav"] a {
            border-radius: 10px;
            margin-bottom: 5px;
            transition: all 0.3s ease;
            background: transparent;
        }
        div[data-testid="stSidebarNav"] a:hover {
            background: rgba(255, 255, 255, 0.05);
            transform: translateX(5px);
            border-left: 3px solid var(--primary);
        }

        /* --- ANIMATIONS --- */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translate3d(0, 30px, 0); }
            to { opacity: 1; transform: translate3d(0, 0, 0); }
        }

        @keyframes pulseGlow {
            0% { box-shadow: 0 0 0 0 rgba(217, 70, 239, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(217, 70, 239, 0); }
            100% { box-shadow: 0 0 0 0 rgba(217, 70, 239, 0); }
        }

        .animate-enter {
            animation: fadeInUp 0.6s ease-out forwards;
        }
        
        .animate-enter-delay-1 {
            animation: fadeInUp 0.6s ease-out 0.2s forwards;
            opacity: 0;
        }
        
        .animate-enter-delay-2 {
            animation: fadeInUp 0.6s ease-out 0.4s forwards;
            opacity: 0;
        }

        /* --- CARD STYLING --- */
        .modern-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        }

        .modern-card:hover {
            transform: translateY(-5px) scale(1.01);
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5);
            border-color: rgba(217, 70, 239, 0.3);
        }

        /* --- BUTTONS --- */
        .stButton button {
            background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            box-shadow: 0 10px 20px -5px rgba(217, 70, 239, 0.4);
            transform: translateY(-2px);
        }

        /* --- HEADERS --- */
        h1, h2, h3 {
            color: var(--text-white);
            font-family: 'Inter', sans-serif;
        }
        
        .gradient-text {
            background: -webkit-linear-gradient(0deg, #D946EF, #8B5CF6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)