import json
from datetime import date, timedelta

import streamlit as st

st.set_page_config(
    page_title="MediTools Pro",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
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

# One consistent app header; avoid repeating the developer credit on every page.
st.markdown(
    '<div class="app-brand">🩺 MediTools Pro <span style="font-weight:400;">| Made by Fazle Azeem · Ayub Medical College</span></div>',
    unsafe_allow_html=True,
)

# A visible hamburger menu is rendered in the main page so it remains easy to find on mobile.
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
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False

menu_col, page_label_col = st.columns([1, 5])
with menu_col:
    if st.button("☰ Menu", key="hamburger_toggle", use_container_width=True):
        st.session_state.menu_open = not st.session_state.menu_open
with page_label_col:
    st.caption(f"Current section: {st.session_state.current_page}")

if st.session_state.menu_open:
    with st.container(border=True):
        st.markdown("**☰ Navigation**")
        selected_page = st.radio(
            "Choose a section",
            PAGES,
            index=PAGES.index(st.session_state.current_page),
            key="main_navigation_radio",
            label_visibility="collapsed",
        )
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.session_state.menu_open = False
            st.rerun()

page = st.session_state.current_page

# Sidebar remains available as an additional navigation option.
with st.sidebar:
    st.title("🩺 MediTools Pro")
    st.caption("Clinical learning toolkit")
    sidebar_page = st.radio(
        "Navigate",
        PAGES,
        index=PAGES.index(st.session_state.current_page),
        key="sidebar_navigation_radio",
    )
    if sidebar_page != st.session_state.current_page:
        st.session_state.current_page = sidebar_page
        st.rerun()
    st.divider()
    st.caption("Ayub Medical College · Abbottabad")

if "history_text" not in st.session_state:
    st.session_state.history_text = ""
if "history_data" not in st.session_state:
    st.session_state.history_data = {}
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
    st.caption("For education only. Do not enter identifiable patient information into a public deployment.")

# -------------------- History Taking --------------------
elif page == "📋 History Taking":
    st.title("📋 Clinical History Taking")
    st.caption("Complete relevant sections for the case. Use 'Not asked', 'Not known', or 'Not applicable' when appropriate.")

    with st.form("history_form"):
        st.subheader("1. Patient identification")
        a, b, c = st.columns(3)
        with a:
            patient_name = st.text_input("Patient name / initials")
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=25)
            sex = st.selectbox("Sex", ["Female", "Male", "Intersex / other", "Not recorded"])
        with b:
            guardian = st.text_input("Father / guardian / spouse name (if relevant)")
            occupation = st.text_input("Occupation")
            marital_status = st.selectbox("Marital status", ["Not recorded", "Single", "Married", "Divorced", "Widowed"])
        with c:
            address = st.text_input("Address / locality (avoid unnecessary identifiers)")
            encounter = st.selectbox("Encounter", ["OPD", "IPD", "Emergency", "Clinic", "Other"])
            ward_bed = st.text_input("Ward / bed number (if relevant)")
        exam_date = st.date_input("Date", value=date.today())

        st.subheader("2. Presenting complaint and history")
        cc = st.text_area("Chief complaint(s) with duration", placeholder="e.g., Fever for 3 days")
        hopi = st.text_area(
            "History of presenting illness (HOPI)",
            height=150,
            placeholder="Onset, duration, progression, site, character, severity, timing, aggravating/relieving factors, associated symptoms, relevant negatives, previous episodes, treatment taken, and effect on daily activities.",
        )
        with st.expander("Guided HOPI builder (optional)", expanded=False):
            st.caption("Use only features relevant to the presenting complaint; the free-text HOPI above is retained.")
            h1, h2, h3 = st.columns(3)
            with h1:
                hopi_onset = st.text_input("Onset", placeholder="Sudden / gradual; date or context")
                hopi_site = st.text_input("Site / radiation", placeholder="Where? Does it radiate?")
                hopi_character = st.text_input("Character", placeholder="Sharp, dull, burning, etc.")
            with h2:
                hopi_duration = st.text_input("Duration / course", placeholder="Duration; intermittent or continuous")
                hopi_severity = st.text_input("Severity", placeholder="e.g., 6/10; effect on function")
                hopi_timing = st.text_input("Timing / pattern", placeholder="Day/night; episodic pattern")
            with h3:
                hopi_aggravating = st.text_input("Aggravating factors")
                hopi_relieving = st.text_input("Relieving factors")
                hopi_associated = st.text_input("Associated symptoms")
            hopi_treatment = st.text_input("Treatment tried and response")
        # Guided HOPI details are incorporated when the main form is submitted.
        guided_hopi_lines = [
            f"Onset: {hopi_onset}", f"Duration/course: {hopi_duration}",
            f"Site/radiation: {hopi_site}", f"Character: {hopi_character}",
            f"Severity: {hopi_severity}", f"Timing/pattern: {hopi_timing}",
            f"Aggravating factors: {hopi_aggravating}", f"Relieving factors: {hopi_relieving}",
            f"Associated symptoms: {hopi_associated}", f"Treatment/response: {hopi_treatment}",
        ]

        relevant_negatives = st.text_area("Important relevant negatives")
        previous_episodes = st.text_area("Previous similar episodes / treatment for current illness")

        st.subheader("3. Past history")
        p1, p2 = st.columns(2)
        with p1:
            past_medical = st.text_area("Past medical history", placeholder="Chronic illnesses, previous admissions, TB, diabetes, hypertension, asthma, seizures, etc.")
            past_surgical = st.text_area("Past surgical / procedural history", placeholder="Operations, procedures, dates, indications, complications, anaesthetic problems.")
            past_psychiatric = st.text_area("Psychiatric history (if relevant)")
        with p2:
            medication_history = st.text_area("Medication history", placeholder="Prescribed, OTC, herbal medicines; dose, route, frequency, adherence, last dose.")
            allergies = st.text_area("Drug / food / other allergies", placeholder="Substance and reaction; document 'No known allergies' only if confirmed.")
            transfusion_history = st.text_area("Blood transfusion history (if relevant)")

        st.subheader("4. Family, personal and social history")
        f1, f2 = st.columns(2)
        with f1:
            family_history = st.text_area("Family history", placeholder="Similar illnesses, diabetes, hypertension, cardiac disease, cancer, genetic conditions; affected relative and age.")
            personal_history = st.text_area("Personal history", placeholder="Diet, appetite, sleep, bowel/bladder habits, activity, and functional status.")
        with f2:
            social_history = st.text_area("Social / environmental history", placeholder="Living situation, support, occupation exposures, travel, animals, housing, and relevant risks.")
            substance_history = st.text_area("Tobacco / vaping / alcohol / other substances", placeholder="Type, amount, frequency, duration; use neutral, nonjudgmental wording.")
            immunization = st.text_area("Immunization history (if relevant)")

        st.subheader("5. Gynecological and obstetric history (when relevant)")
        g1, g2 = st.columns(2)
        with g1:
            gyn_history = st.text_area("Gynecological history", placeholder="Menarche, cycle regularity, duration/flow, LMP, dysmenorrhea, discharge, contraception, cervical screening.")
        with g2:
            obstetric_history = st.text_area("Obstetric history", placeholder="Gravidity/parity, pregnancy outcomes, complications, antenatal care, current pregnancy details.")
            sexual_history = st.text_area("Sexual history (when clinically relevant and appropriate)", placeholder="Ask sensitively, with consent and privacy.")

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
            ros_skin_endo_heme = st.text_area("Skin / endocrine / hematological / other", placeholder="Rash, itch, heat/cold intolerance, thirst, bruising, bleeding, lymph nodes, other relevant systems.")

        st.subheader("7. Summary")
        summary = st.text_area("Clinical summary / problem representation")
        provisional_diagnosis = st.text_area("Provisional diagnosis / differential (if appropriate)")
        informant = st.text_input("Informant and reliability", placeholder="e.g., patient; reliable")
        submit_history = st.form_submit_button("Generate history", type="primary", use_container_width=True)

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
                "HOPI: " + "\\n".join(
                    ([hopi.strip()] if hopi.strip() else [])
                    + [line for line in guided_hopi_lines if line.split(": ", 1)[1].strip()]
                ) if (hopi.strip() or any(line.split(": ", 1)[1].strip() for line in guided_hopi_lines)) else "HOPI: Not recorded",
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
            ("Family, personal and social history", [
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
        # Keep the in-session list manageable.
        st.session_state.saved_cases = st.session_state.saved_cases[:50]
        st.success("History generated and added to this session's case list. Review it for accuracy before use.")
        st.text_area("Generated history preview", value=history_text, height=420)
        st.download_button(
            "⬇️ Download history (.txt)",
            data=history_text,
            file_name="clinical_history.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.download_button(
            "⬇️ Download structured data (.json)",
            data=json.dumps({"history": history_text}, ensure_ascii=False, indent=2),
            file_name="clinical_history.json",
            mime="application/json",
            use_container_width=True,
        )

# -------------------- Calculators --------------------
elif page == "🧮 Medical Calculators":
    st.title("🧮 Medical Calculators")
    st.warning("For learning and decision support only. Verify results with current clinical guidance; do not use a calculator alone to make treatment decisions.")
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
            # CKD-EPI 2021 race-free creatinine equation; intended for adults.
            if eg_sex == "Female":
                k, alpha, sex_factor = 0.7, -0.241, 1.012
            else:
                k, alpha, sex_factor = 0.9, -0.302, 1.0
            egfr = 142 * (min(scr / k, 1) ** alpha) * (max(scr / k, 1) ** -1.200) * (0.9938 ** eg_age) * sex_factor
            st.metric("Estimated eGFR", f"{egfr:.1f} mL/min/1.73 m²")
            st.caption("This is an estimate for adults, not a diagnosis. Interpretation depends on clinical context and persistence over time; creatinine-based estimates may be unreliable in pregnancy, acute kidney injury, unusual muscle mass, and other situations.")

    with tabs[2]:
        st.subheader("Weight-based dose arithmetic")
        st.caption("Enter a dose already prescribed or verified from a trusted pediatric reference. This tool does not select a medicine dose.")
        child_weight = st.number_input("Child weight (kg)", min_value=0.1, max_value=200.0, value=10.0, step=0.1, key="dose_weight")
        mgkg = st.number_input("Verified prescribed dose (mg/kg per dose)", min_value=0.0, max_value=1000.0, value=0.0, step=0.1, key="dose_mgkg")
        max_dose = st.number_input("Maximum dose per dose (mg; 0 = no cap entered)", min_value=0.0, max_value=100000.0, value=0.0, step=1.0, key="dose_max")
        if st.button("Calculate arithmetic result", key="dose_calc"):
            if mgkg <= 0:
                st.error("Enter a verified dose greater than zero.")
            else:
                dose = child_weight * mgkg
                if max_dose > 0:
                    dose = min(dose, max_dose)
                st.metric("Calculated amount per dose", f"{dose:.2f} mg")
                st.warning("Confirm the medicine, indication, age limits, formulation, frequency, maximum daily dose, renal/hepatic adjustments, and local guideline before use.")

    with tabs[3]:
        st.subheader("Estimated due date (EDD)")
        lmp = st.date_input("First day of last menstrual period (LMP)", value=date.today(), key="lmp_date")
        if st.button("Calculate EDD", key="edd_calc"):
            edd = lmp + timedelta(days=280)
            st.metric("Estimated due date", edd.strftime("%d %b %Y"))
            st.caption("Assumes a 28-day cycle and is an estimate; clinical dating may be adjusted using ultrasound and pregnancy history.")

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
            st.caption("Record components as well as the total. Adapt assessment for intubation, language barriers, sedation, or other limitations.")

# -------------------- OSCE --------------------
elif page == "🩺 OSCE Checklist":
    st.title("🩺 OSCE Checklist")
    system = st.selectbox("Choose examination", ["General examination", "Cardiovascular", "Respiratory", "Abdominal", "Neurological"])
    checklists = {
        "General examination": ["Hand hygiene and introduce yourself", "Confirm identity and obtain consent", "Assess general appearance and distress", "Observe vital signs", "Check pallor, jaundice, cyanosis, clubbing, edema, and lymph nodes as indicated", "Thank the patient and summarize findings"],
        "Cardiovascular": ["Hand hygiene, introduction, consent, position", "General inspection and vital signs", "Hands and pulse", "Face and neck / JVP", "Precordial inspection and palpation", "Auscultate valve areas; assess added sounds and murmurs", "Peripheral pulses and edema", "Thank patient and present findings"],
        "Respiratory": ["Hand hygiene, introduction, consent, position", "General inspection and respiratory rate", "Hands, face, neck, and trachea", "Chest inspection", "Palpation: expansion and tactile vocal fremitus as appropriate", "Percussion", "Auscultation and vocal resonance", "Thank patient and present findings"],
        "Abdominal": ["Hand hygiene, introduction, consent, ask about pain, expose appropriately", "General inspection and hands", "Inspect abdomen", "Auscultate if indicated by local teaching protocol", "Percuss abdomen and assess liver/spleen as indicated", "Palpate lightly then deeply; assess organs/masses", "Check for ascites and hernias when indicated", "Thank patient and present findings"],
        "Neurological": ["Hand hygiene, introduction, consent, assess alertness", "Cranial nerves", "Motor system: bulk, tone, power", "Reflexes and plantar response", "Sensory examination", "Coordination and gait when safe", "Adapt examination to symptoms and summarize findings"],
    }
    st.caption("Educational checklist; follow your institution's examination sequence and patient-safety requirements.")
    for item in checklists[system]:
        st.checkbox(item, key=f"osce_{system}_{item}")

# -------------------- Drug Reference --------------------
elif page == "💊 Drug Reference":
    st.title("💊 Drug Reference")
    st.warning("Examples for revision only—not prescribing advice. Doses depend on indication, age, weight, formulation, allergies, organ function, and local guidance.")
    st.table({
        "Medicine": ["Paracetamol / acetaminophen", "Amoxicillin"],
        "Reminder": [
            "Check age/weight-specific dosing, liver disease, combination products, and maximum daily dose.",
            "Check indication, allergy history, local antimicrobial guidance, renal function, and formulation.",
        ],
    })
    st.info("A safe drug-dose module should use a verified, maintained drug database rather than a short hard-coded dose list.")

# -------------------- Lab Values --------------------
elif page == "🧪 Lab Values":
    st.title("🧪 Lab Values")
    st.caption("Illustrative adult reference intervals only. Ranges vary by laboratory, age, sex, pregnancy, and clinical context.")
    st.table({
        "Test": ["Hemoglobin (adult male)", "Hemoglobin (adult female, non-pregnant)", "WBC", "Platelets", "Sodium", "Potassium", "Creatinine"],
        "Illustrative reference interval": ["~13.5–17.5 g/dL", "~12.0–15.5 g/dL", "~4.0–11.0 ×10⁹/L", "~150–400 ×10⁹/L", "~135–145 mmol/L", "~3.5–5.0 mmol/L", "Lab- and patient-dependent"],
    })
    st.caption("Always use the reporting laboratory's own reference range and interpret results clinically.")

# -------------------- Downloads --------------------
elif page == "📥 Downloads":
    st.title("📥 Downloads")
    if st.session_state.history_text:
        st.success("Your most recently generated history is ready.")
        st.download_button(
            "⬇️ Download history (.txt)",
            data=st.session_state.history_text,
            file_name="clinical_history.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.download_button(
            "⬇️ Download history (.json)",
            data=json.dumps({"history": st.session_state.history_text}, ensure_ascii=False, indent=2),
            file_name="clinical_history.json",
            mime="application/json",
            use_container_width=True,
        )
    else:
        st.info("Generate a history first from the History Taking page; it will then appear here during this session.")

    st.divider()
    st.subheader("Session case library")
    st.caption("Cases are stored only in the current Streamlit session and may disappear when the session resets. This is not a secure medical-record system.")
    if st.session_state.saved_cases:
        search_term = st.text_input("Search session cases by name or complaint")
        filtered_cases = [
            case for case in st.session_state.saved_cases
            if search_term.lower() in (case["patient"] + " " + case["complaint"]).lower()
        ]
        st.write(f"{len(filtered_cases)} matching case(s)")
        for index, case in enumerate(filtered_cases):
            with st.expander(f'{case["patient"]} · {case["age"]} y · {case["complaint"]} · {case["created_at"]}'):
                st.text_area("Case history", value=case["history"], height=220, key=f"case_preview_{index}")
                st.download_button(
                    "Download this case",
                    data=case["history"],
                    file_name=f"clinical_case_{index + 1}.txt",
                    mime="text/plain",
                    key=f"case_download_{index}",
                )
        st.download_button(
            "Download all session cases as JSON",
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
st.caption("MediTools Pro · Educational use")
