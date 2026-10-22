import json
from datetime import date, timedelta
import streamlit as st

st.set_page_config(
    page_title="MediTools Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .app-brand {text-align: center; padding: .35rem 0 .75rem 0; font-size: .95rem; font-weight: 650;}
    h1 {font-size: 1.8rem !important;} h2 {font-size: 1.4rem !important;} h3 {font-size: 1.15rem !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-brand">🩺 MediTools Pro <span style="font-weight:400;">| Made by Fazle Azeem · Ayub Medical College</span></div>',
    unsafe_allow_html=True,
)

PAGES = [
    "🏠 Home",
    "📋 History Taking",
    "🧮 Medical Calculators",
    "🩺 OSCE Checklist",
    "💊 Drug Reference",
    "🧪 Lab Values",
    "📥 Downloads",
]

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

with st.sidebar:
    st.title("🩺 MediTools Pro")
    st.caption("Clinical learning toolkit")
    st.radio("Navigate", PAGES, key="current_page")
    st.divider()
    st.caption("Made by Fazle Azeem")
    st.caption("Ayub Medical College · Abbottabad")

page = st.session_state.current_page
st.caption(f"Current section: {page}")

if "history_text" not in st.session_state:
    st.session_state.history_text = ""
if "saved_cases" not in st.session_state:
    st.session_state.saved_cases = []

# -------------------- Home - CLEAN NO BLUE BOX --------------------
if page == "🏠 Home":
    st.title("MediTools Pro")
    st.caption("Clinical learning toolkit · Ayub Medical College")
    st.write("A practical workspace for clinical history taking, examination practice, and basic medical calculations.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Clinical documentation", "History")
    c2.metric("Calculators", "4 tools")
    c3.metric("Study resources", "OSCE & labs")

# -------------------- History Taking --------------------
elif page == "📋 History Taking":
    st.title("📋 Clinical History Taking")
    st.caption("Biodata order as per Ayub Medical College format.")

    with st.form("history_form"):
        st.subheader("1. Patient Biodata (Identification)")

        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            patient_name = st.text_input("Patient Name / Initials *")
        with r1c2:
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=25)
        with r1c3:
            sex = st.selectbox("Sex / Gender", ["Male", "Female", "Other", "Not recorded"])

        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed", "Not recorded"])
        with r2c2:
            if sex == "Female" and marital_status == "Married":
                fh_label = "Husband Name (W/O - Wife Of)"
                fh_placeholder = "e.g., W/O Muhammad Ali"
                relation_prefix = "W/O"
            elif sex == "Female" and marital_status in ["Divorced", "Widowed"]:
               
