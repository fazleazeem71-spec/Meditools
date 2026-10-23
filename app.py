import json
from datetime import date, timedelta

import streamlit as st

# Streamlit page configuration must run before other Streamlit UI commands.
st.set_page_config(
    page_title="MediTools Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from auth import check_login, supabase  # Keep your existing authentication module.
from secure_history import run_secure_history  # Keep your existing secure-history module.

# Initialize app state before authentication code accesses session_state.
defaults = {
    "current_page": "Home",
    "menu_open": False,
    "history_text": "",
    "saved_cases": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

check_login()

PAGES = [
    "Home",
    "History Taking",
    "Secure History",
    "Medical Calculators",
    "OSCE Checklist",
    "Drug Reference",
    "Lab Values",
    "Downloads",
]

PAGE_ICONS = {
    "Home": "⌂",
    "History Taking": "▤",
    "Secure History": "▣",
    "Medical Calculators": "∑",
    "OSCE Checklist": "✓",
    "Drug Reference": "Rx",
    "Lab Values": "◉",
    "Downloads": "↓",
}

# -------------------- Styling --------------------
st.markdown(
    """
    <style>
    .app-brand {
        text-align: center;
        padding: .35rem 0 .85rem 0;
        font-size: 1.02rem;
        font-weight: 700;
        letter-spacing: .01em;
    }
    .app-subtitle {
        text-align: center;
        color: #687386;
        font-size: .88rem;
        margin-top: -.45rem;
        margin-bottom: 1rem;
    }
    div[data-testid="stMetric"] {
        padding: .55rem .65rem;
        border: 1px solid rgba(128,128,128,.22);
        border-radius: 12px;
    }
    div[data-testid="stMetricLabel"] { font-size: .85rem; }
    div[data-testid="stMetricValue"] { font-size: 1.3rem; }
    div.stButton > button { border-radius: 9px; }
    div[data-testid="stFormSubmitButton"] > button { border-radius: 9px; }
    .section-note { color: #687386; font-size: .9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-brand">MediTools Pro</div>'
    '<div class="app-subtitle">Clinical learning toolkit · Ayub Medical College</div>',
    unsafe_allow_html=True,
)

# -------------------- Session state --------------------
# A single navigation state avoids the stale selection problem caused by two
# separate radio widgets trying to control the same page.
def choose_page():
    chosen = st.session_state.get("navigation_choice", "Home")
    if chosen in PAGES:
        st.session_state.current_page = chosen
    st.session_state.menu_open = False

# -------------------- Hamburger navigation --------------------
menu_col, current_col = st.columns([1, 5], vertical_alignment="center")
with menu_col:
    if st.button("☰  Menu", key="hamburger_menu", use_container_width=True):
        st.session_state.menu_open = not st.session_state.menu_open
with current_col:
    st.caption(f"Current section  /  {st.session_state.current_page}")

if st.session_state.menu_open:
    with st.container(border=True):
        st.markdown("#### Navigation")
        st.caption("Choose a section")
        st.radio(
            "Navigation options",
            options=PAGES,
            format_func=lambda item: f"{PAGE_ICONS[item]}   {item}",
            key="navigation_choice",
            index=PAGES.index(st.session_state.current_page),
            on_change=choose_page,
            label_visibility="collapsed",
        )

page = st.session_state.current_page

# Optional compact sidebar information; navigation is intentionally kept in
# the hamburger panel so the two controls cannot get out of sync.
with st.sidebar:
    st.markdown("## MediTools Pro")
    st.caption("Clinical learning toolkit")
    st.divider()
    st.caption(f"Current section: **{page}**")
    st.caption("Made by Fazle Azeem")
    st.caption("Ayub Medical College · Abbottabad")

# -------------------- Home --------------------
if page == "Home":
    st.title("Home")
    st.success("Welcome to MediTools Pro")
    st.write(
        "A student-oriented workspace for clinical history taking, examination "
        "practice, medical calculations, and quick-reference learning."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Clinical documentation", "History taking")
    c2.metric("Calculators", "5 tools")
    c3.metric("Revision resources", "OSCE and labs")

    st.divider()
    st.subheader("Workspace")
    cards = [
        ("History Taking", "Create a structured clinical history and download a text or JSON summary."),
        ("Secure History", "Open the separate secure-history workflow configured in your project."),
        ("Medical Calculators", "BMI, adult eGFR estimate, weight-based dose arithmetic, EDD, and GCS."),
        ("OSCE Checklist", "Use checklists for general, cardiovascular, respiratory, abdominal, and neurological examinations."),
        ("Drug Reference", "Review concise safety reminders for commonly encountered medicines."),
        ("Lab Values", "Review illustrative adult laboratory reference intervals."),
        ("Downloads", "Retrieve the latest history and session cases."),
    ]
    for title, description in cards:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(description)

    st.info(
        "Educational use only. Do not enter identifiable patient information into a public or shared deployment. "
        "Use your institution's approved systems for real patient records."
    )

# -------------------- History Taking --------------------
elif page == "History Taking":
    st.title("Clinical History Taking")
    st.caption(
        "Complete relevant sections. Use 'Not asked', 'Not known', or 'Not applicable' where appropriate."
    )

    with st.form("history_form"):
        st.subheader("1. Patient identification")
        a, b, c = st.columns(3)
        with a:
            patient_name = st.text_input("Patient name / initials")
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=25)
            sex = st.selectbox("Sex", ["Female", "Male", "Intersex / other", "Not recorded"])
        with b:
            guardian = st.text_input("Father / guardian / spouse (if relevant)")
            occupation = st.text_input("Occupation")
            marital_status = st.selectbox(
                "Marital status",
                ["Not recorded", "Single", "Married", "Divorced", "Widowed"],
            )
        with c:
            address = st.text_input("Address / locality (avoid unnecessary identifiers)")
            encounter = st.selectbox("Encounter", ["OPD", "IPD", "Emergency", "Clinic", "Other"])
            ward_bed = st.text_input("Ward / bed (if relevant)")
        exam_date = st.date_input("Date", value=date.today())
        informant = st.text_input("Informant and reliability", placeholder="e.g., patient; reliable")

        st.subheader("2. Presenting complaint and history")
        cc = st.text_area("Chief complaint(s) with duration", placeholder="e.g., Fever for 3 days")
        hopi = st.text_area(
            "History of presenting illness (HOPI)",
            height=145,
            placeholder=(
                "Onset, duration, progression, site, character, severity, timing, "
                "aggravating/relieving factors, associated symptoms, relevant negatives, "
                "previous episodes, treatment, and effect on daily activities."
            ),
        )
        relevant_negatives = st.text_area("Important relevant negatives")
        previous_episodes = st.text_area("Previous similar episodes / treatment for current illness")

        st.subheader("3. Past history")
        p1, p2 = st.columns(2)
        with p1:
            past_medical = st.text_area(
                "Past medical history",
                placeholder="Chronic illnesses, admissions, TB, diabetes, hypertension, asthma, seizures, etc.",
            )
            past_surgical = st.text_area(
                "Past surgical / procedural history",
                placeholder="Operations, procedures, dates, indications, complications, anaesthetic problems.",
            )
            past_psychiatric = st.text_area("Psychiatric history (if relevant)")
        with p2:
            medication_history = st.text_area(
                "Medication history",
                placeholder="Prescribed, OTC, and herbal medicines; dose, route, frequency, adherence, last dose.",
            )
            allergies = st.text_area(
                "Drug / food / other allergies",
                placeholder="Record substance and reaction. State 'no known allergies' only if confirmed.",
            )
            transfusion_history = st.text_area("Blood transfusion history (if relevant)")

        st.subheader("4. Family, personal, and social history")
        f1, f2 = st.columns(2)
        with f1:
            family_history = st.text_area("Family history")
            personal_history = st.text_area(
                "Personal history", placeholder="Diet, appetite, sleep, bowel/bladder habits, activity, function."
            )
        with f2:
            social_history = st.text_area(
                "Social / environmental history",
                placeholder="Living situation, support, occupation exposures, travel, animals, housing, relevant risks.",
            )
            substance_history = st.text_area(
                "Tobacco / vaping / alcohol / other substances",
                placeholder="Type, amount, frequency, and duration; use neutral wording.",
            )
            immunization = st.text_area("Immunization history (if relevant)")

        st.subheader("5. Gynecological and obstetric history")
        g1, g2 = st.columns(2)
        with g1:
            gyn_history = st.text_area(
                "Gynecological history",
                placeholder="Menarche, cycle, flow, LMP, dysmenorrhea, discharge, contraception, screening.",
            )
        with g2:
            obstetric_history = st.text_area(
                "Obstetric history",
                placeholder="Gravidity/parity, pregnancy outcomes, complications, antenatal care.",
            )
            sexual_history = st.text_area(
                "Sexual history (when clinically relevant and appropriate)",
                placeholder="Ask sensitively, with consent and privacy.",
            )

        st.subheader("6. Review of systems")
        r1, r2 = st.columns(2)
        with r1:
            ros_general = st.text_area("General", placeholder="Fever, weight change, fatigue, appetite, night sweats.")
            ros_cvs = st.text_area("Cardiovascular", placeholder="Chest pain, palpitations, dyspnea, orthopnea, PND, edema, syncope.")
            ros_resp = st.text_area("Respiratory", placeholder="Cough, sputum, wheeze, hemoptysis, dyspnea, pleuritic pain.")
            ros_git = st.text_area("Gastrointestinal", placeholder="Pain, nausea/vomiting, swallowing, bowel change, bleeding, jaundice.")
        with r2:
            ros_cns = st.text_area("Neurological", placeholder="Headache, weakness, sensory change, seizures, loss of consciousness.")
            ros_msk = st.text_area("Musculoskeletal", placeholder="Joint pain/swelling, stiffness, muscle pain, limitation.")
            ros_uro = st.text_area("Genitourinary", placeholder="Dysuria, frequency, urgency, hematuria, flank pain.")
            ros_skin_endo_heme = st.text_area(
                "Skin / endocrine / hematological / other",
                placeholder="Rash, itch, heat/cold intolerance, thirst, bruising, bleeding, lymph nodes.",
            )

        st.subheader("7. Vitals and examination")
        v1, v2, v3 = st.columns(3)
        with v1:
            bp = st.text_input("Blood pressure", placeholder="e.g., 120/80 mmHg")
            pulse = st.text_input("Pulse", placeholder="e.g., 80/min, regular")
            respiratory_rate = st.text_input("Respiratory rate", placeholder="e.g., 16/min")
        with v2:
            temperature = st.text_input("Temperature", placeholder="e.g., 37.0 °C")
            spo2 = st.text_input("SpO₂", placeholder="e.g., 98% on room air")
            pain_score = st.text_input("Pain score", placeholder="e.g., 3/10")
        with v3:
            weight_height = st.text_input("Weight / height", placeholder="e.g., 65 kg / 170 cm")
            capillary_glucose = st.text_input("Capillary glucose", placeholder="Value and units")
            other_vitals = st.text_input("Other observations")
        general_exam = st.text_area("General examination findings")
        systemic_exam = st.text_area("Systemic examination findings")
        investigations = st.text_area("Investigations and results")

        st.subheader("8. Clinical assessment and plan")
        summary = st.text_area("Clinical summary / problem representation")
        provisional_diagnosis = st.text_area("Provisional diagnosis")
        differential_diagnosis = st.text_area("Differential diagnoses")
        management_plan = st.text_area("Initial plan / further assessment")

        submit_history = st.form_submit_button(
            "Generate history", type="primary", use_container_width=True
        )

    if submit_history:
        sections = [
            ("Patient identification", [
                f"Name / initials: {patient_name or 'Not recorded'}",
                f"Age: {age} years",
                f"Sex: {sex}",
                f"Father / guardian / spouse: {guardian or 'Not recorded'}",
                f"Occupation: {occupation or 'Not recorded'}",
                f"Marital status: {marital_status}",
                f"Address / locality: {address or 'Not recorded'}",
                f"Encounter: {encounter}",
                f"Ward / bed: {ward_bed or 'Not applicable'}",
                f"Date: {exam_date}",
                f"Informant / reliability: {informant or 'Not recorded'}",
            ]),
            ("Presenting complaint and HOPI", [
                f"Chief complaint(s): {cc or 'Not recorded'}",
                f"HOPI:\n{hopi or 'Not recorded'}",
                f"Relevant negatives: {relevant_negatives or 'Not recorded'}",
                f"Previous episodes / treatment: {previous_episodes or 'Not recorded'}",
            ]),
            ("Past history", [
                f"Past medical history: {past_medical or 'Not recorded'}",
                f"Past surgical / procedural history: {past_surgical or 'Not recorded'}",
                f"Psychiatric history: {past_psychiatric or 'Not recorded'}",
                f"Medication history: {medication_history or 'Not recorded'}",
                f"Allergies: {allergies or 'Not recorded'}",
                f"Transfusion history: {transfusion_history or 'Not recorded'}",
            ]),
            ("Family, personal, and social history", [
                f"Family history: {family_history or 'Not recorded'}",
                f"Personal history: {personal_history or 'Not recorded'}",
                f"Social / environmental history: {social_history or 'Not recorded'}",
                f"Substance history: {substance_history or 'Not recorded'}",
                f"Immunization: {immunization or 'Not recorded'}",
            ]),
            ("Gynecological and obstetric history", [
                f"Gynecological history: {gyn_history or 'Not applicable / not recorded'}",
                f"Obstetric history: {obstetric_history or 'Not applicable / not recorded'}",
                f"Sexual history: {sexual_history or 'Not applicable / not recorded'}",
            ]),
            ("Review of systems", [
                f"General: {ros_general or 'Not recorded'}",
                f"Cardiovascular: {ros_cvs or 'Not recorded'}",
                f"Respiratory: {ros_resp or 'Not recorded'}",
                f"Gastrointestinal: {ros_git or 'Not recorded'}",
                f"Neurological: {ros_cns or 'Not recorded'}",
                f"Musculoskeletal: {ros_msk or 'Not recorded'}",
                f"Genitourinary: {ros_uro or 'Not recorded'}",
                f"Skin / endocrine / hematological / other: {ros_skin_endo_heme or 'Not recorded'}",
            ]),
            ("Vitals and examination", [
                f"Blood pressure: {bp or 'Not recorded'}",
                f"Pulse: {pulse or 'Not recorded'}",
                f"Respiratory rate: {respiratory_rate or 'Not recorded'}",
                f"Temperature: {temperature or 'Not recorded'}",
                f"SpO2: {spo2 or 'Not recorded'}",
                f"Pain score: {pain_score or 'Not recorded'}",
                f"Weight / height: {weight_height or 'Not recorded'}",
                f"Capillary glucose: {capillary_glucose or 'Not recorded'}",
                f"Other observations: {other_vitals or 'Not recorded'}",
                f"General examination: {general_exam or 'Not recorded'}",
                f"Systemic examination: {systemic_exam or 'Not recorded'}",
                f"Investigations: {investigations or 'Not recorded'}",
            ]),
            ("Clinical assessment and plan", [
                f"Clinical summary: {summary or 'Not recorded'}",
                f"Provisional diagnosis: {provisional_diagnosis or 'Not recorded'}",
                f"Differential diagnoses: {differential_diagnosis or 'Not recorded'}",
                f"Initial plan: {management_plan or 'Not recorded'}",
            ]),
        ]

        history_text = "MEDITOOLS PRO — CLINICAL HISTORY\n" + "=" * 34 + "\n\n"
        for heading, lines in sections:
            history_text += heading.upper() + "\n" + "\n".join(lines) + "\n\n"

        st.session_state.history_text = history_text
        st.session_state.saved_cases.insert(0, {
            "created_at": str(date.today()),
            "patient": patient_name or "Unnamed case",
            "age": age,
            "sex": sex,
            "complaint": cc or "No complaint entered",
            "history": history_text,
        })
        st.session_state.saved_cases = st.session_state.saved_cases[:50]

        st.success("History generated. Review it for accuracy before clinical use.")
        st.text_area(
            "Generated history preview",
            value=history_text,
            height=420,
            key="generated_history_preview",
        )
        st.download_button(
            "Download history (.txt)",
            data=history_text,
            file_name="clinical_history.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.download_button(
            "Download structured data (.json)",
            data=json.dumps({"history": history_text}, ensure_ascii=False, indent=2),
            file_name="clinical_history.json",
            mime="application/json",
            use_container_width=True,
        )

# -------------------- Secure History --------------------
elif page == "Secure History":
    st.title("Secure History")
    st.caption("This section is provided by your separate secure_history.py module.")
    # The function signature is defined by your existing module; this assumes
    # run_secure_history() takes no arguments, as suggested by your import.
    run_secure_history()

# -------------------- Medical Calculators --------------------
elif page == "Medical Calculators":
    st.title("Medical Calculators")
    st.warning(
        "For learning and decision support only. Verify results with current clinical guidance. "
        "Do not use a calculator alone to make treatment decisions."
    )
    tabs = st.tabs(["BMI", "eGFR", "Child dose", "EDD", "GCS"])

    with tabs[0]:
        st.subheader("Body Mass Index (BMI)")
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=400.0, value=70.0, step=0.5, key="bmi_weight")
        height = st.number_input("Height (cm)", min_value=30.0, max_value=250.0, value=170.0, step=0.5, key="bmi_height")
        if st.button("Calculate BMI", key="bmi_calc"):
            bmi = weight / ((height / 100) ** 2)
            st.metric("BMI", f"{bmi:.1f} kg/m²")
            if bmi < 18.5:
                st.caption("Adult classification: underweight")
            elif bmi < 25:
                st.caption("Adult classification: healthy-weight range")
            elif bmi < 30:
                st.caption("Adult classification: overweight")
            else:
                st.caption("Adult classification: obesity range")
            st.caption("Adult BMI categories are not interpreted the same way for children or in every clinical context.")

    with tabs[1]:
        st.subheader("Estimated GFR — CKD-EPI 2021 creatinine equation")
        eg_age = st.number_input("Age (years)", min_value=18, max_value=120, value=40, key="eg_age")
        eg_sex = st.selectbox("Sex used by equation", ["Female", "Male"], key="eg_sex")
        scr = st.number_input("Serum creatinine (mg/dL)", min_value=0.1, max_value=30.0, value=1.0, step=0.1, key="scr")
        if st.button("Estimate eGFR", key="egfr_calc"):
            if eg_sex == "Female":
                k, alpha, sex_factor = 0.7, -0.241, 1.012
            else:
                k, alpha, sex_factor = 0.9, -0.302, 1.0
            egfr = 142 * (min(scr / k, 1) ** alpha) * (max(scr / k, 1) ** -1.200) * (0.9938 ** eg_age) * sex_factor
            st.metric("Estimated eGFR", f"{egfr:.1f} mL/min/1.73 m²")
            st.caption(
                "Adult estimate only, not a diagnosis. Interpretation depends on clinical context and persistence. "
                "Creatinine-based estimates may be unreliable in pregnancy, acute kidney injury, unusual muscle mass, "
                "and other situations."
            )

    with tabs[2]:
        st.subheader("Weight-based dose arithmetic")
        st.caption("Enter a dose already prescribed or verified from a trusted pediatric reference. This tool does not select a medicine dose.")
        child_weight = st.number_input("Child weight (kg)", min_value=0.1, max_value=200.0, value=10.0, step=0.1, key="dose_weight")
        mgkg = st.number_input("Verified prescribed dose (mg/kg per dose)", min_value=0.0, max_value=1000.0, value=0.0, step=0.1, key="dose_mgkg")
        max_dose = st.number_input("Maximum dose per dose (mg; 0 = no cap entered)", min_value=0.0, max_value=100000.0, value=0.0, step=1.0, key="dose_max")
        if st.button("Calculate dose arithmetic", key="dose_calc"):
            if mgkg <= 0:
                st.error("Enter a verified dose greater than zero.")
            else:
                dose = child_weight * mgkg
                if max_dose > 0:
                    dose = min(dose, max_dose)
                st.metric("Calculated amount per dose", f"{dose:.2f} mg")
                st.warning("Confirm medicine, indication, age limits, formulation, frequency, maximum daily dose, organ adjustments, and local guidance.")

    with tabs[3]:
        st.subheader("Estimated due date (EDD)")
        lmp = st.date_input("First day of last menstrual period (LMP)", value=date.today(), key="lmp_date")
        if st.button("Calculate EDD", key="edd_calc"):
            edd = lmp + timedelta(days=280)
            st.metric("Estimated due date", edd.strftime("%d %b %Y"))
            st.caption("Assumes a 28-day cycle. Clinical dating may be adjusted using ultrasound and pregnancy history.")

    with tabs[4]:
        st.subheader("Glasgow Coma Scale (GCS)")
        eye_options = {"4 — Spontaneous": 4, "3 — To sound": 3, "2 — To pressure": 2, "1 — None": 1}
        verbal_options = {"5 — Oriented": 5, "4 — Confused": 4, "3 — Words": 3, "2 — Sounds": 2, "1 — None": 1}
        motor_options = {"6 — Obeys commands": 6, "5 — Localizes": 5, "4 — Normal flexion / withdraws": 4, "3 — Abnormal flexion": 3, "2 — Extension": 2, "1 — None": 1}
        eye_label = st.selectbox("Eye response", list(eye_options), key="gcs_eye")
        verbal_label = st.selectbox("Verbal response", list(verbal_options), key="gcs_verbal")
        motor_label = st.selectbox("Motor response", list(motor_options), key="gcs_motor")
        if st.button("Calculate GCS", key="gcs_calc"):
            total = eye_options[eye_label] + verbal_options[verbal_label] + motor_options[motor_label]
            st.metric("GCS total", f"{total}/15")
            st.caption(f"E{eye_options[eye_label]} · V{verbal_options[verbal_label]} · M{motor_options[motor_label]}")
            st.caption("Record components as well as total; adapt assessment for intubation, language barriers, sedation, or other limitations.")

# -------------------- OSCE Checklist --------------------
elif page == "OSCE Checklist":
    st.title("OSCE Checklist")
    system = st.selectbox(
        "Choose examination",
        ["General examination", "Cardiovascular", "Respiratory", "Abdominal", "Neurological"],
    )
    checklists = {
        "General examination": [
            "Hand hygiene and introduce yourself",
            "Confirm identity and obtain consent",
            "Assess general appearance and distress",
            "Observe vital signs",
            "Check pallor, jaundice, cyanosis, clubbing, edema, and lymph nodes as indicated",
            "Thank the patient and summarize findings",
        ],
        "Cardiovascular": [
            "Hand hygiene, introduction, consent, position",
            "General inspection and vital signs",
            "Hands and pulse",
            "Face and neck / JVP",
            "Precordial inspection and palpation",
            "Auscultate valve areas; assess added sounds and murmurs",
            "Peripheral pulses and edema",
            "Thank patient and present findings",
        ],
        "Respiratory": [
            "Hand hygiene, introduction, consent, position",
            "General inspection and respiratory rate",
            "Hands, face, neck, and trachea",
            "Chest inspection",
            "Palpation: expansion and tactile vocal fremitus as appropriate",
            "Percussion",
            "Auscultation and vocal resonance",
            "Thank patient and present findings",
        ],
        "Abdominal": [
            "Hand hygiene, introduction, consent, ask about pain, expose appropriately",
            "General inspection and hands",
            "Inspect abdomen",
            "Auscultate if indicated by local teaching protocol",
            "Percuss abdomen and assess liver/spleen as indicated",
            "Palpate lightly then deeply; assess organs/masses",
            "Check for ascites and hernias when indicated",
            "Thank patient and present findings",
        ],
        "Neurological": [
            "Hand hygiene, introduction, consent, assess alertness",
            "Cranial nerves",
            "Motor system: bulk, tone, power",
            "Reflexes and plantar response",
            "Sensory examination",
            "Coordination and gait when safe",
            "Adapt examination to symptoms and summarize findings",
        ],
    }
    st.caption("Educational checklist; follow your institution's examination sequence and patient-safety requirements.")
    for item in checklists[system]:
        st.checkbox(item, key=f"osce_{system}_{item}")

# -------------------- Drug Reference --------------------
elif page == "Drug Reference":
    st.title("Drug Reference")
    st.warning(
        "Educational reminders only—not prescribing advice. Doses depend on indication, age, weight, "
        "formulation, allergies, organ function, and local guidance."
    )
    st.table({
        "Medicine": ["Paracetamol / acetaminophen", "Amoxicillin"],
        "Safety reminder": [
            "Check age/weight-specific dosing, liver disease, combination products, and maximum daily dose.",
            "Check indication, allergy history, local antimicrobial guidance, renal function, and formulation.",
        ],
    })
    st.info("A safe drug-dose module should use a verified, maintained drug database rather than a short hard-coded list.")

# -------------------- Lab Values --------------------
elif page == "Lab Values":
    st.title("Lab Values")
    st.caption("Illustrative adult reference intervals only. Ranges vary by laboratory, age, sex, pregnancy, and clinical context.")
    st.table({
        "Test": [
            "Hemoglobin (adult male)",
            "Hemoglobin (adult female, non-pregnant)",
            "WBC",
            "Platelets",
            "Sodium",
            "Potassium",
            "Creatinine",
        ],
        "Illustrative reference interval": [
            "~13.5–17.5 g/dL",
            "~12.0–15.5 g/dL",
            "~4.0–11.0 ×10⁹/L",
            "~150–400 ×10⁹/L",
            "~135–145 mmol/L",
            "~3.5–5.0 mmol/L",
            "Laboratory- and patient-dependent",
        ],
    })
    st.caption("Always use the reporting laboratory's own reference range and interpret results clinically.")

# -------------------- Downloads --------------------
elif page == "Downloads":
    st.title("Downloads")
    if st.session_state.history_text:
        st.success("Your most recently generated history is ready.")
        st.download_button(
            "Download history (.txt)",
            data=st.session_state.history_text,
            file_name="clinical_history.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.download_button(
            "Download history (.json)",
            data=json.dumps({"history": st.session_state.history_text}, ensure_ascii=False, indent=2),
            file_name="clinical_history.json",
            mime="application/json",
            use_container_width=True,
        )
    else:
        st.info("Generate a history first from History Taking; it will then appear here during this session.")

    st.divider()
    st.subheader("Session case library")
    st.caption(
        "Cases are stored only in the current Streamlit session and may disappear when it resets. "
        "This is not a secure medical-record system."
    )
    if st.session_state.saved_cases:
        search_term = st.text_input("Search cases by name or complaint", key="case_search")
        filtered_cases = [
            case for case in st.session_state.saved_cases
            if search_term.casefold() in (
                case["patient"] + " " + case["complaint"]
            ).casefold()
        ]
        st.write(f"{len(filtered_cases)} matching case(s)")
        for index, case in enumerate(filtered_cases):
            with st.expander(
                f'{case["patient"]} · {case["age"]} y · {case["complaint"]} · {case["created_at"]}'
            ):
                st.text_area(
                    "Case history",
                    value=case["history"],
                    height=220,
                    key=f"case_preview_{index}",
                )
                st.download_button(
                    "Download this case",
                    data=case["history"],
                    file_name=f"clinical_case_{index + 1}.txt",
                    mime="text/plain",
                    key=f"case_download_{index}",
                )
        st.download_button(
            "Download all session cases (.json)",
            data=json.dumps(st.session_state.saved_cases, ensure_ascii=False, indent=2),
            file_name="meditools_session_cases.json",
            mime="application/json",
            use_container_width=True,
        )
        if st.button("Clear session case list", type="secondary"):
            st.session_state.saved_cases = []
            st.session_state.history_text = ""
            st.rerun()
    else:
        st.caption("No cases saved in this session yet.")

st.divider()
st.caption("MediTools Pro · Educational use · Made by Fazle Azeem · Ayub Medical College, Abbottabad")
