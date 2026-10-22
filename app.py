import streamlit as st
from datetime import date

st.set_page_config(page_title="MediTools - Ayub", layout="wide", page_icon="🩺")
st.title("🩺 MediTools - History Taking")
st.caption("Made for Ward Use | Ayub Medical College")

# --- SESSION STATE FOR DYNAMIC LABEL ---
if 'sex' not in st.session_state:
    st.session_state.sex = "Male"

# ---------- 1. BIO DATA ----------
st.header("1. Bio Data")
c1,c2,c3 = st.columns(3)

with c1:
    name = st.text_input("Name")
    sex = st.selectbox("Sex", ["Male","Female","Other"], key="sex")
    # DYNAMIC LABEL - THIS IS THE FIX
    if sex == "Male":
        fh_label = "Father Name"
    elif sex == "Female":
        fh_label = "Husband Name (Father if unmarried)"
    else:
        fh_label = "Father / Guardian Name"
    father_husband = st.text_input(fh_label)

with c2:
    # AGE WITH + AND - , DEFAULT 25
    age = st.number_input("Age (years)", min_value=0, max_value=110, value=25, step=1)
    address = st.text_input("Address")
    occupation = st.text_input("Occupation")

with c3:
    mode = st.selectbox("Mode", ["OPD","IPD","ER"])
    exam_date = st.date_input("Date", value=date.today())
    ward_bed = st.text_input("Ward / Bed No.")

# ---------- 2. HISTORY ----------
st.header("2. History")

chief_complaint = st.text_area("Chief Complaint (C/C)", placeholder="e.g. Fever for 3 days...", height=80)

st.subheader("HOPI - History of Present Illness")
hopi = st.text_area("HOPI", placeholder="Onset, duration, progression, associated symptoms, aggravating/relieving factors...", height=150)

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

# ---------- 3. SYSTEMIC REVIEW ----------
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

# ---------- GENERATE ----------
st.divider()
if st.button("📋 Generate Full History", type="primary"):
    st.success("History Generated Successfully!")
    st.subheader(f"Patient: {name} | {age}Y / {sex} | {fh_label}: {father_husband}")
    st.write(f"**Mode:** {mode} | **Date:** {exam_date} | **Ward:** {ward_bed} | **Address:** {address} | **Job:** {occupation}")
    st.write(f"**C/C:** {chief_complaint}")
    st.write(f"**HOPI:** {hopi}")
    st.write(f"**Past Med:** {past_med} | **Surgical:** {past_surg}")
    st.write(f"**Drug:** {drug_history} | **Allergy:** {allergy}")
    st.write(f"**Family:** {family_history}")
    st.write(f"**Personal:** {personal_history}")
    st.write(f"**Menstrual:** {menstrual_history}")

st.info("Tip: Age now has + / - with default 25. And Father/Husband changes automatically with Sex!")
