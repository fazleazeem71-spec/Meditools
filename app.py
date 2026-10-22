import json
from datetime import date, timedelta
import streamlit as st

st.set_page_config(
    page_title="MediTools Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Styling --------------------
st.markdown(
    """
    <style>
    .app-brand {
        text-align: center;
        padding: .35rem 0 .75rem 0;
        font-size: .95rem;
        font-weight: 650;
        letter-spacing: .01em;
    }
    h1 { font-size: 1.8rem !important; line-height: 1.25 !important; }
    h2 { font-size: 1.4rem !important; line-height: 1.3 !important; }
    h3 { font-size: 1.15rem !important; line-height: 1.35 !important; }
    div[data-testid="stMetric"] { padding: .2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.35rem !important; }
    div[data-testid="stMetricLabel"] { font-size: .85rem !important; }
    .stMarkdown, .stCaption, label { line-height: 1.55; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-brand">🩺 MediTools Pro <span style="font-weight:400;">| Made by Fazle Azeem · Ayub Medical College</span></div>',
    unsafe_allow_html=True,
)

# -------------------- FIXED NAVIGATION --------------------
PAGES = [
    "🏠 Home",
    "📋 History Taking",
    "🧮 Medical Calculators",
    "🩺 OSCE Checklist",
    "💊 Drug Reference",
    "🧪 Lab Values",
    "📥 Downloads",
]

# Single source of truth for navigation - no double rerun
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# Sidebar is the ONLY navigation - this fixes the bug
with st.sidebar:
    st.title("🩺 MediTools Pro")
    st.caption("Clinical learning toolkit")
    st.radio(
        "Navigate",
        PAGES,
        key="current_page",
    )
    st.divider()
    st.caption("Made by Fazle Azeem")
    st.caption("Ayub Medical College · Abbottabad")

page = st.session_state.current_page
st.caption(f"Current section: {page}")

if "history_text" not in st.session_state:
    st.session_state.history_text = ""
if "saved_cases" not in st.session_state:
    st.session_state.saved_cases = []

# -------------------- Home --------------------
if page == "🏠 Home":
    st.title("MediTools Pro")
    st.caption("Clinical learning toolkit · Ayub Medical College")
    st.write("A practical workspace for clinical history taking, examination practice, and basic medical calculations.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Clinical documentation", "History")
    c2.metric("Calculators", "4 tools")
    c3.metric("Study resources", "OSCE & labs")
    st.divider()
    st.subheader("Quick navigation")
    quick_items = [
        ("📋 History Taking", "Structured patient history, examination findings, assessment, and downloadable notes."),
        ("🧮 Medical Calculators", "BMI, adult eGFR estimate, due date, GCS, and weight-based dose arithmetic."),
        ("🩺 OSCE Checklist", "Examination checklists for general, cardiovascular, respiratory, abdominal, and neurological exams."),
        ("💊 Drug Reference & 🧪 Lab Values", "Concise educational reminders; confirm all clinical decisions with current references."),
        ("📥 Downloads", "Access histories generated during the current session."),
    ]
    for title, description in quick_items:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(description)
