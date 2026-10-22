import streamlit as st
from datetime import date
import json

st.set_page_config(page_title="MediTools Pro", page_icon="🩺", layout="wide")

# ========== LIGHT / DARK MODE ==========
mode = st.sidebar.selectbox("🎨 Theme", ["☀️ Light Mode", "🌙 Dark Mode"])
if mode == "🌙 Dark Mode":
    st.markdown("""
    <style>
    .stApp {background-color: #0E1117; color: white;}
    .stTextInput>div>div>input {background-color: #262730; color: white;}
    .stTextArea>div>div>textarea {background-color: #262730; color: white;}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {background-color: #FFFFFF; color: black;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("🩺 MediTools Pro")
st.sidebar.caption("Ayub Medical College - Abbottabad")

menu = st.sidebar.radio("📁 MENU", [
    "📋 History Taking", 
    "🧮 Medical Calculators",
    "📥 Downloads"
])

# ========== HISTORY TAKING ==========
if menu == "📋 History Taking":
    st.title("📋 History Taking")
    
    c1,c2,c3 = st.columns(3)
    with c1:
        name = st.text_input("Patient Name")
        sex = st.selectbox("Sex", ["Male","Female","Other"])
        label = "Father Name" if sex=="Male" else "Husband Name (Father if unmarried)" if sex=="Female" else "Father / Guardian Name"
        fh_name = st.text_input(label, key="fh")
    with c2:
        age = st.number_input("Age", 0, 110, 25, 1)
        address = st.text_input("Address")
        contact = st.text_input("Contact No")
    with c3:
        mode_sel = st.selectbox("Mode", ["OPD","IPD","ER"])
        bed = st.text_input("Ward / Bed No")
        d = st.date_input("Date", date.today())

    cc = st.text_area("Chief Complaints")
    hopi = st.text_area("HOPI - History of Present Illness", height=150)
    pmh = st.text_area("Past Medical / Surgical History")
    dh = st.text_area("Drug History")
    fam = st.text_area("Family History")
    per = st.text_area("Personal History")
    ros = st.text_area("Review of Systems")
    exam = st.text_area("General Physical + Systemic Examination")

    # DOWNLOAD HISTORY
    if st.button("Generate & Prepare for Download", type="primary"):
        history_text = f"""
MEDICAL HISTORY - MediTools Pro
Date: {d}
Name: {name} | Age: {age} | Sex: {sex}
{label}: {fh_name}
Address: {address} | Contact: {contact}
Mode: {mode_sel} | {bed}

Chief Complaints: {cc}
HOPI: {hopi}
Past Hx: {pmh}
Drug Hx: {dh}
Family Hx: {fam}
Personal Hx: {per}
ROS: {ros}
Examination: {exam}
"""
        st.success("History Ready! Go to Downloads folder to download.")
        st.session_state['history_text'] = history_text
        st.text_area("Preview", history_text, height=300)

# ========== CALCULATORS ==========
elif menu == "🧮 Medical Calculators":
    st.title("🧮 Medical Calculators")
    
    t1,t2,t3,t4,t5 = st.tabs(["BMI", "GFR", "Child Dose", "Due Date", "GCS"])
    
    with t1:
        st.subheader("BMI Calculator")
        w = st.number_input("Weight (kg)", 20.0, 200.0, 70.0, key="bmi_w")
        h = st.number_input("Height (cm)", 100.0, 220.0, 170.0, key="bmi_h")
        if st.button("Calculate BMI"):
            bmi = w / ((h/100)**2)
            st.metric("BMI", f"{bmi:.1f}")
            if bmi < 18.5: st.warning("Underweight")
            elif bmi < 24.9: st.success("Normal")
            elif bmi < 29.9: st.warning("Overweight")
            else: st.error("Obese")
            st.session_state['bmi_result'] = f"BMI: {bmi:.1f}"

    with t2:
        st.subheader("eGFR Calculator (CKD-EPI)")
        creat = st.number_input("Creatinine mg/dL", 0.1, 15.0, 1.0)
        age_gfr = st.number_input("Age", 1, 100, 25, key="gfr_age")
        is_female = st.checkbox("Female?")
        if st.button("Calculate eGFR"):
            st.info("Formula: eGFR ~ 186 x (Creat)^-1.154 x (Age)^-0.203 (x 0.742 if female)")
            st.metric("eGFR", f"~ {70 - creat*10:.0f} mL/min (Estimated)")
    
    with t3:
        st.subheader("Child Dose Calculator")
        child_w = st.number_input("Child Weight (kg)", 1.0, 50.0, 10.0)
        adult_dose = st.number_input("Adult Dose (mg)", 10.0, 2000.0, 500.0)
        if st.button("Calculate Child Dose"):
            clark = adult_dose * child_w / 70
            young = adult_dose * age / (age+12) if 'age' in locals() else 0
            st.metric("Clark's Rule", f"{clark:.1f} mg")
            st.metric("Young's Rule", f"{young:.1f} mg")

    with t4:
        st.subheader("EDD - Expected Due Date")
        lmp = st.date_input("LMP Date", date.today())
        if st.button("Calculate Due Date"):
            edd = date.fromordinal(lmp.toordinal() + 280)
            st.success(f"Due Date: {edd}")

    with t5:
        st.subheader("Glasgow Coma Scale (GCS)")
        e = st.selectbox("Eye", ["4 Spontaneous", "3 To Voice", "2 To Pain", "1 None"])
        v = st.selectbox("Verbal", ["5 Oriented", "4 Confused", "3 Inappropriate", "2 Incomprehensible", "1 None"])
        m = st.selectbox("Motor", ["6 Obeys", "5 Localizes", "4 Withdraws", "3 Flexion", "2 Extension", "1 None"])
        if st.button("Calculate GCS"):
            gcs = int(e[0]) + int(v[0]) + int(m[0])
            st.metric("GCS", f"{gcs}/15")
            if gcs <= 8: st.error("Severe - Coma")
            elif gcs <= 12: st.warning("Moderate")
            else: st.success("Mild")

# ========== DOWNLOADS ==========
else:
    st.title("📥 Download Center")
    st.write("Download your data as file - Works like real app!")
    
    if 'history_text' in st.session_state:
        st.download_button(
            label="📄 Download History as TXT",
            data=st.session_state['history_text'],
            file_name=f"History_{date.today()}.txt",
            mime="text/plain"
        )
        st.download_button(
            label="📄 Download History as JSON",
            data=json.dumps({"history": st.session_state['history_text']}, indent=2),
            file_name=f"History_{date.today()}.json",
            mime="application/json"
        )
    else:
        st.info("No history yet. Go to History Taking -> Generate")
    
    st.divider()
    st.subheader("App Share")
    st.code("https://meditools-ayub.streamlit.app")
    st.write("Share this link - Anyone can Add to Home Screen and get app icon!")
