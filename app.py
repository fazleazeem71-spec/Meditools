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
    .app-brand {
        text-align: center;
        padding: .35rem 0 .75rem 0;
        font-size: .95rem;
        font-weight: 650;
    }
    h1 { font-size: 1.8rem !important; }
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

if page == "🏠 Home":
    st.title("MediTools Pro")
    st.caption("Clinical learning toolkit · Ayub Medical College")
    st.write("A practical workspace for clinical history taking, examination practice, and basic medical calculations.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Clinical documentation", "History")
    c2.metric("Calculators", "4 tools")
    c3.metric("Study resources", "OSCE & labs")
    st.info("Open sidebar >> top left to navigate. For education only.")

elif page == "📋 History Taking":
    st.title("📋 Clinical History Taking")
    with st.form("history_form"):
        a, b, c = st.columns(3)
        with a:
            patient_name = st.text_input("Patient name / initials")
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=25)
            sex = st.selectbox("Sex", ["Female", "Male", "Intersex / other", "Not recorded"])
        with b:
            guardian = st.text_input("Father / guardian / spouse name")
            occupation = st.text_input("Occupation")
            marital_status = st.selectbox("Marital status", ["Not recorded", "Single", "Married", "Divorced", "Widowed"])
        with c:
            address = st.text_input("Address / locality")
            encounter = st.selectbox("Encounter", ["OPD", "IPD", "Emergency", "Clinic", "Other"])
            ward_bed = st.text_input("Ward / bed number")
        exam_date = st.date_input("Date", value=date.today())
        cc = st.text_area("Chief complaint(s) with duration")
        hopi = st.text_area("HOPI", height=120)
        with st.expander("Guided HOPI builder (optional)"):
            h1, h2, h3 = st.columns(3)
            with h1:
                hopi_onset = st.text_input("Onset")
                hopi_site = st.text_input("Site / radiation")
                hopi_character = st.text_input("Character")
            with h2:
                hopi_duration = st.text_input("Duration / course")
                hopi_severity = st.text_input("Severity")
                hopi_timing = st.text_input("Timing / pattern")
            with h3:
                hopi_aggravating = st.text_input("Aggravating factors")
                hopi_relieving = st.text_input("Relieving factors")
                hopi_associated = st.text_input("Associated symptoms")
            hopi_treatment = st.text_input("Treatment tried and response")
        relevant_negatives = st.text_area("Important relevant negatives")
        previous_episodes = st.text_area("Previous similar episodes")
        p1, p2 = st.columns(2)
        with p1:
            past_medical = st.text_area("Past medical history")
            past_surgical = st.text_area("Past surgical history")
            past_psychiatric = st.text_area("Psychiatric history")
        with p2:
            medication_history = st.text_area("Medication history")
            allergies = st.text_area("Allergies")
            transfusion_history = st.text_area("Transfusion history")
        f1, f2 = st.columns(2)
        with f1:
            family_history = st.text_area("Family history")
            personal_history = st.text_area("Personal history")
        with f2:
            social_history = st.text_area("Social history")
            substance_history = st.text_area("Tobacco / alcohol / substances")
            immunization = st.text_area("Immunization")
        g1, g2 = st.columns(2)
        with g1:
            gyn_history = st.text_area("Gynecological history")
        with g2:
            obstetric_history = st.text_area("Obstetric history")
            sexual_history = st.text_area("Sexual history")
        r1, r2 = st.columns(2)
        with r1:
            ros_general = st.text_area("General ROS")
            ros_cvs = st.text_area("Cardiovascular ROS")
            ros_resp = st.text_area("Respiratory ROS")
            ros_git = st.text_area("GIT ROS")
        with r2:
            ros_cns = st.text_area("Neurological ROS")
            ros_msk = st.text_area("MSK ROS")
            ros_uro = st.text_area("GU ROS")
            ros_skin = st.text_area("Skin / other ROS")
        st.subheader("Vitals and examination")
        v1, v2, v3, v4 = st.columns(4)
        with v1:
            bp = st.text_input("Blood pressure")
            pulse = st.text_input("Pulse")
            respiratory_rate = st.text_input("Respiratory rate")
        with v2:
            temperature = st.text_input("Temperature")
            spo2 = st.text_input("SpO2")
            pain_score = st.text_input("Pain score")
        with v3:
            weight_height = st.text_input("Weight / height")
            capillary_glucose = st.text_input("Glucose")
            other_vitals = st.text_input("Other observations")
        with v4:
            general_exam = st.text_area("General exam")
            systemic_exam = st.text_area("Systemic exam")
            investigations = st.text_area("Investigations")
        summary = st.text_area("Clinical summary")
        provisional_diagnosis = st.text_area("Provisional diagnosis")
        differential_diagnosis = st.text_area("DDx")
        management_plan = st.text_area("Initial plan")
        informant = st.text_input("Informant")
        submit_history = st.form_submit_button("Generate history", type="primary", use_container_width=True)

    if submit_history:
        guided = [f"Onset: {hopi_onset}", f"Duration: {hopi_duration}", f"Site: {hopi_site}", f"Character: {hopi_character}", f"Severity: {hopi_severity}", f"Timing: {hopi_timing}", f"Agg: {hopi_aggravating}", f"Rel: {hopi_relieving}", f"Assoc: {hopi_associated}", f"Treat: {hopi_treatment}"]
        hopi_combined = "\n".join(([hopi.strip()] if hopi.strip() else []) + [l for l in guided if l.split(": ",1)[1].strip()])
        history_text = f"MEDITOOLS PRO — CLINICAL HISTORY\nDate: {exam_date}\nName: {patient_name}\nAge: {age} Sex: {sex}\nComplaint: {cc}\nHOPI: {hopi_combined or hopi}\nPast: {past_medical}\nMeds: {medication_history}\nAllergies: {allergies}\nFamily: {family_history}\nROS: {ros_general} {ros_cvs}\nVitals: BP {bp} Pulse {pulse} RR {respiratory_rate} Temp {temperature} SpO2 {spo2}\nExam: {general_exam} {systemic_exam}\nInvestigations: {investigations}\nSummary: {summary}\nDiagnosis: {provisional_diagnosis}\nDDx: {differential_diagnosis}\nPlan: {management_plan}\n"
        st.session_state.history_text = history_text
        st.session_state.saved_cases.insert(0, {"created_at": str(date.today()), "patient": patient_name or "Unnamed", "age": age, "sex": sex, "complaint": cc or "No complaint", "history": history_text})
        st.success("History generated!")
        st.text_area("Preview", value=history_text, height=400)
        st.download_button("⬇️ Download .txt", data=history_text, file_name="history.txt")

elif page == "🧮 Medical Calculators":
    st.title("🧮 Medical Calculators")
    tabs = st.tabs(["BMI", "eGFR", "Child dose", "EDD", "GCS"])
    with tabs[0]:
        w = st.number_input("Weight kg", 1.0, 400.0, 70.0, key="bmi_w")
        h = st.number_input("Height cm", 30.0, 250.0, 170.0, key="bmi_h")
        if st.button("Calculate BMI", key="bmi_c"):
            st.metric("BMI", f"{w/((h/100)**2):.1f}")
    with tabs[1]:
        eg_age = st.number_input("Age", 18, 120, 40, key="eg_age")
        eg_sex = st.selectbox("Sex", ["Female", "Male"], key="eg_sex")
        scr = st.number_input("Creatinine mg/dL", 0.1, 30.0, 1.0, key="scr")
        if st.button("Estimate eGFR", key="egfr_c"):
            k, a, sf = (0.7, -0.241, 1.012) if eg_sex=="Female" else (0.9, -0.302, 1.0)
            egfr = 142 * (min(scr/k,1)**a) * (max(scr/k,1)**-1.2) * (0.9938**eg_age) * sf
            st.metric("eGFR", f"{egfr:.1f}")
    with tabs[2]:
        cw = st.number_input("Child weight kg", 0.1, 200.0, 10.0, key="dose_w")
        mgkg = st.number_input("Dose mg/kg", 0.0, 1000.0, 0.0, key="dose_mg")
        if st.button("Calculate dose", key="dose_c"):
            st.metric("Dose", f"{cw*mgkg:.2f} mg")
    with tabs[3]:
        lmp = st.date_input("LMP", value=date.today(), key="lmp")
        if st.button("Calculate EDD", key="edd_c"):
            st.metric("EDD", (lmp + timedelta(days=280)).strftime("%d %b %Y"))
    with tabs[4]:
        eye = st.selectbox("Eye", [4,3,2,1], key="gcs_e")
        verbal = st.selectbox("Verbal", [5,4,3,2,1], key="gcs_v")
        motor = st.selectbox("Motor", [6,5,4,3,2,1], key="gcs_m")
        if st.button("Calculate GCS", key="gcs_c"):
            st.metric("GCS", f"{eye+verbal+motor}/15")

elif page == "🩺 OSCE Checklist":
    st.title("🩺 OSCE Checklist")
    system = st.selectbox("Exam", ["General", "Cardiovascular", "Respiratory", "Abdominal", "Neurological"])
    items = {
        "General": ["Hand hygiene", "Introduce, consent", "General appearance", "Vitals", "Thank patient"],
        "Cardiovascular": ["Hand hygiene, consent", "Inspection, vitals", "Hands, pulse", "JVP", "Precordial exam", "Auscultate"],
        "Respiratory": ["Hand hygiene, consent", "Inspection", "Hands, face, neck", "Chest inspection", "Percussion", "Auscultation"],
        "Abdominal": ["Hand hygiene, consent", "Inspection", "Auscultate", "Palpate", "Percuss"],
        "Neurological": ["Hand hygiene, consent", "Cranial nerves", "Motor", "Reflexes", "Sensory", "Gait"]
    }
    for it in items[system]:
        st.checkbox(it, key=f"osce_{system}_{it}")

elif page == "💊 Drug Reference":
    st.title("💊 Drug Reference")
    st.table({"Medicine": ["Paracetamol", "Amoxicillin"], "Reminder": ["Check dosing", "Check allergy"]})

elif page == "🧪 Lab Values":
    st.title("🧪 Lab Values")
    st.table({"Test": ["Hb M", "Hb F", "WBC", "Platelets", "Na", "K"], "Range": ["13.5-17.5", "12-15.5", "4-11", "150-400", "135-145", "3.5-5.0"]})

elif page == "📥 Downloads":
    st.title("📥 Downloads")
    if st.session_state.history_text:
        st.download_button("⬇️ Download", data=st.session_state.history_text, file_name="history.txt")
    else:
        st.info("Generate history first.")

st.divider()
st.caption("MediTools Pro © 2026 · Made by Fazle Azeem · Ayub Medical College, Abbottabad")
