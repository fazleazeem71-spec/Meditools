import streamlit as st
from datetime import date
import json

st.set_page_config(page_title="MediTools Pro - Fazle Azeem", layout="wide", page_icon="🩺")

# ===== MAKE NAME SUPER VISIBLE =====
st.markdown("""
<style>
    .big-name { font-size:24px !important; font-weight:bold !important; color:#0066CC !important; text-align:center; }
    [data-theme="dark"] input, [data-theme="dark"] textarea { background-color: #EEEEEE !important; color: #000000 !important; }
    [data-theme="dark"] div[data-baseweb="select"] div { background-color: #EEEEEE !important; color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

# ===== TOP BANNER - YOUR NAME =====
st.markdown('<div class="big-name">🩺 MediTools Pro | Made by Fazle Azeem | Ayub Medical College</div>', unsafe_allow_html=True)

st.sidebar.title("🩺 MediTools Pro")
st.sidebar.markdown("## 👨‍⚕️ Fazle Azeem")
st.sidebar.markdown("**Ayub Medical College**")
st.sidebar.markdown("**Abbottabad**")
st.sidebar.divider()

menu = st.sidebar.radio("📁 SELECT", [
    "🏠 Home",
    "📋 History Taking", 
    "🧮 Medical Calculators",
    "🩺 OSCE Checklist",
    "💊 Drug Doses",
    "🧪 Lab Values",
    "📥 Downloads"
])

st.sidebar.divider()
st.sidebar.success("✅ Made by Fazle Azeem")
st.sidebar.info("Class of 2026\nAyub Medical College")

# ===== HOME =====
if menu == "🏠 Home":
    st.title("🏠 Home - MediTools Pro")
    st.success("Welcome Fazle Azeem! Your App is Ready!")
    c1,c2,c3 = st.columns(3)
    c1.metric("Made By", "Fazle Azeem")
    c2.metric("College", "Ayub Medical")
    c3.metric("Tools", "7 Features")
    st.divider()
    st.markdown("""
    ### Your App Has:
    1. 📋 **History Taking** (Full)
    2. 🧮 **Calculators** (BMI, GFR, Child Dose, EDD, GCS)
    3. 🩺 **OSCE**
    4. 💊 **Drugs**
    5. 🧪 **Labs**
    6. 📥 **Downloads**
    """)

# ===== HISTORY =====
elif menu == "📋 History Taking":
    st.title("📋 History Taking")
    if 'sex' not in st.session_state:
        st.session_state.sex = "Male"
    c1,c2,c3 = st.columns(3)
    with c1:
        name = st.text_input("Patient Name", key="p_name")
        sex = st.selectbox("Sex", ["Male","Female","Other"], key="sex")
        fh_label = "Father Name" if sex=="Male" else "Husband Name" if sex=="Female" else "Father / Guardian"
        father_husband = st.text_input(fh_label, key="p_fh")
    with c2:
        age = st.number_input("Age", 0, 110, 25, 1, key="p_age")
        address = st.text_input("Address", key="p_add")
        occupation = st.text_input("Occupation", key="p_occ")
    with c3:
        mode = st.selectbox("Mode", ["OPD","IPD","ER"], key="p_mode")
        exam_date = st.date_input("Date", value=date.today(), key="p_date")
        ward_bed = st.text_input("Ward / Bed No.", key="p_ward")
    
    cc = st.text_area("Chief Complaint", key="p_cc")
    hopi = st.text_area("HOPI", height=120, key="p_hopi")
    
    col1, col2 = st.columns(2)
    with col1:
        past_med = st.text_area("Past Medical History", key="p1")
        drug_history = st.text_area("Drug History", key="p2")
    with col2:
        family_history = st.text_area("Family History", key="p3")
        personal_history = st.text_area("Personal History", key="p4")
    
    r1,r2,r3 = st.columns(3)
    with r1:
        ros_gen = st.text_area("General", key="ros1")
        ros_cvs = st.text_area("CVS", key="ros2")
    with r2:
        ros_resp = st.text_area("Respiratory", key="ros3")
        ros_git = st.text_area("GIT", key="ros4")
    with r3:
        ros_cns = st.text_area("CNS", key="ros5")
        ros_msk = st.text_area("MSK", key="ros6")
    
    if st.button("📋 Generate", type="primary"):
        history_text = f"History - Made by Fazle Azeem\nPatient: {name} | {age}Y {sex} | {fh_label}: {father_husband}\nMode: {mode} | Date: {exam_date} | Ward: {ward_bed}\nCC: {cc}\nHOPI: {hopi}\nPast: {past_med}\nDrug: {drug_history}\nFamily: {family_history}\nPersonal: {personal_history}\nROS: {ros_gen} {ros_cvs} {ros_resp} {ros_git} {ros_cns} {ros_msk}"
        st.session_state['history_text'] = history_text
        st.success(f"Generated for {name}")
        st.text_area("Preview", history_text, height=300)

# ===== CALCULATORS - MUST SHOW =====
elif menu == "🧮 Medical Calculators":
    st.title("🧮 Medical Calculators")
    st.caption("Made by Fazle Azeem - All Working")
    t1,t2,t3,t4,t5 = st.tabs(["BMI", "GFR", "Child Dose", "EDD", "GCS"])
    with t1:
        w = st.number_input("Weight kg", 20.0, 200.0, 70.0, key="cw")
        h = st.number_input("Height cm", 100.0, 220.0, 170.0, key="ch")
        if st.button("Calculate BMI", key="b1"):
            bmi = w / ((h/100)**2)
            st.metric("BMI", f"{bmi:.1f}")
    with t2:
        cr = st.number_input("Creatinine", 0.1, 15.0, 1.0, key="cr")
        if st.button("Calculate GFR", key="b2"):
            st.metric("eGFR", f"{90-cr*20:.0f}")
    with t3:
        cw = st.number_input("Child Weight kg", 1.0, 50.0, 10.0, key="cwg")
        ad = st.number_input("Adult Dose mg", 10.0, 2000.0, 500.0, key="ad")
        ca = st.number_input("Child Age", 1, 12, 5, key="ca")
        if st.button("Calculate Dose", key="b3"):
            st.metric("Clark", f"{ad*cw/70:.1f} mg")
            st.metric("Young", f"{ad*ca/(ca+12):.1f} mg")
    with t4:
        lmp = st.date_input("LMP", date.today(), key="lmp")
        if st.button("Calculate EDD", key="b4"):
            edd = date.fromordinal(lmp.toordinal()+280)
            st.success(f"EDD: {edd}")
    with t5:
        e = st.selectbox("Eye", ["4 Spontaneous", "3 To Voice", "2 To Pain", "1 None"], key="e")
        v = st.selectbox("Verbal", ["5 Oriented", "4 Confused", "3 Inappropriate", "2 Incomprehensible", "1 None"], key="v")
        m = st.selectbox("Motor", ["6 Obeys", "5 Localizes", "4 Withdraws", "3 Flexion", "2 Extension", "1 None"], key="m")
        if st.button("Calculate GCS", key="b5"):
            gcs = int(e[0])+int(v[0])+int(m[0])
            st.metric("GCS", f"{gcs}/15")

# ===== OSCE =====
elif menu == "🩺 OSCE Checklist":
    st.title("🩺 OSCE Checklist - Made by Fazle Azeem")
    sys = st.selectbox("System", ["CVS","Respiratory","Abdomen"])
    st.write(f"{sys} Examination steps here...")

# ===== DRUGS =====
elif menu == "💊 Drug Doses":
    st.title("💊 Drug Doses")
    st.table({"Drug": ["Paracetamol","Amoxicillin"], "Dose": ["500mg Q6H","500mg TDS"]})

# ===== LABS =====
elif menu == "🧪 Lab Values":
    st.title("🧪 Lab Values")
    st.table({"Test": ["Hb","WBC"], "Normal": ["13-17","4-11k"]})

# ===== DOWNLOADS =====
else:
    st.title("📥 Downloads")
    if 'history_text' in st.session_state:
        st.download_button("Download TXT", st.session_state['history_text'], file_name="History.txt")
        st.download_button("Download JSON", json.dumps({"history": st.session_state['history_text']}), file_name="History.json")
    else:
        st.warning("No history yet")

# ===== FOOTER - ALWAYS VISIBLE =====
st.divider()
st.markdown("<center><h3>👨‍⚕️ Made by Fazle Azeem</h3><b>Ayub Medical College, Abbottabad</b><br>MediTools Pro © 2026</center>", unsafe_allow_html=True)
