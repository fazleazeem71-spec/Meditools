import streamlit as st
from datetime import date
import json

st.set_page_config(page_title="MediTools - Ayub", layout="wide", page_icon="🩺")

# ========== DARK MODE FIX - Makes boxes visible in Dark ==========
st.markdown("""
<style>
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        border-radius: 10px !important;
        border: 1px solid #888888 !important;
    }
    /* FIX: In dark, make input LIGHT GREY with BLACK TEXT - Always readable */
    [data-theme="dark"] input, [data-theme="dark"] textarea {
        background-color: #EEEEEE !important;
        color: #000000 !important;
    }
    [data-theme="dark"] div[data-baseweb="select"] div {
        background-color: #EEEEEE !important;
        color: #000000 !important;
    }
    label { font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

if 'sex' not in st.session_state:
    st.session_state.sex = "Male"

st.sidebar.title("🩺 MediTools Pro")
st.sidebar.caption("Ayub Medical College - Abbottabad")
st.sidebar.success("Dark mode FIXED!")

menu = st.sidebar.radio("📁 MENU", ["📋 History Taking", "🧮 Medical Calculators", "📥 Downloads"])

# ========== 1. YOUR ORIGINAL FULL HISTORY TAKING - RESTORED ==========
if menu == "📋 History Taking":
    st.title("🩺 MediTools - History Taking")
    st.caption("Made for Ward Use | Ayub Medical College")

    st.header("1. Bio Data")
    c1,c2,c3 = st.columns(3)
    with c1:
        name = st.text_input("Name")
        sex = st.selectbox("Sex", ["Male","Female","Other"], key="sex")
        if sex == "Male":
            fh_label = "Father Name"
        elif sex == "Female":
            fh_label = "Husband Name (Father if unmarried)"
        else:
            fh_label = "Father / Guardian Name"
        father_husband = st.text_input(fh_label)
    with c2:
        age = st.number_input("Age (years)", min_value=0, max_value=110, value=25, step=1)
        address = st.text_input("Address")
        occupation = st.text_input("Occupation")
    with c3:
        mode = st.selectbox("Mode", ["OPD","IPD","ER"])
        exam_date = st.date_input("Date", value=date.today())
        ward_bed = st.text_input("Ward / Bed No.")

    st.header("2. History")
    chief_complaint = st.text_area("Chief Complaint (C/C)", placeholder="e.g. Fever for 3 days...", height=80)
    st.subheader("HOPI - History of Present Illness")
    hopi = st.text_area("HOPI", placeholder="Onset, duration, progression...", height=150)

    col1, col2 = st.columns(2)
    with col1:
        past_med = st.text_area("Past Medical History", placeholder="DM, HTN, TB, Surgery...")
        past_surg = st.text_area("Past Surgical History")
        drug_history = st.text_area("Drug History")
        allergy = st.text_area("Allergy History")
    with col2:
        family_history = st.text_area("Family History")
        personal_history = st.text_area("Personal History (Smoking, Alcohol, Diet, Bowel, Bladder, Sleep)")
        menstrual_history = st.text_area("Menstrual / Obstetric History (if Female)")
        socio_history = st.text_area("Socioeconomic History")

    st.header("3. Review of Systems (ROS)")
    r1,r2,r3 = st.columns(3)
    with r1:
        ros_gen = st.text_area("General / Fever / Weight loss")
        ros_cvs = st.text_area("CVS")
        ros_resp = st.text_area("Respiratory")
    with r2:
        ros_git = st.text_area("GIT")
        ros_gut = st.text_area("Genitourinary")
        ros_cns = st.text_area("CNS")
    with r3:
        ros_msk = st.text_area("Musculoskeletal")
        ros_skin = st.text_area("Skin / Others")

    st.divider()
    if st.button("📋 Generate Full History", type="primary"):
        history_text = f"""
MEDICAL HISTORY - MediTools Pro
Date: {exam_date} | Mode: {mode} | Ward: {ward_bed}
Patient: {name} | {age}Y / {sex} | {fh_label}: {father_husband}
Address: {address} | Occupation: {occupation}

Chief Complaint: {chief_complaint}
HOPI: {hopi}
Past Medical: {past_med}
Past Surgical: {past_surg}
Drug: {drug_history} | Allergy: {allergy}
Family: {family_history}
Personal: {personal_history}
Menstrual: {menstrual_history}
Socioeconomic: {socio_history}

ROS:
General: {ros_gen} | CVS: {ros_cvs} | Resp: {ros_resp}
GIT: {ros_git} | GUT: {ros_gut} | CNS: {ros_cns}
MSK: {ros_msk} | Skin: {ros_skin}
"""
        st.success("History Generated Successfully!")
        st.session_state['history_text'] = history_text
        st.text_area("Preview (for Download)", history_text, height=400)
       
