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

# -------------------- Navigation Setup (Corrected) --------------------
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

# Callback function to handle page selection safely without manual reruns
def update_page(key):
    st.session_state.current_page = st.session_state[key]
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
        st.radio(
            "Choose a section",
            PAGES,
            index=PAGES.index(st.session_state.current_page),
            key="main_navigation_radio",
            label_visibility="collapsed",
            on_change=update_page,
            args=("main_navigation_radio",),
        )

page = st.session_state.current_page

# Sidebar navigation option
with st.sidebar:
    st.title("🩺 MediTools Pro")
    st.caption("Clinical learning toolkit")
    st.radio(
        "Navigate",
        PAGES,
        index=PAGES.index(st.session_state.current_page),
        key="sidebar_navigation_radio",
        on_change=update_page,
        args=("sidebar_navigation_radio",),
    )
    st.divider()
    st.caption("Made by Fazle Azeem")
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
        height = st.number_input("Height (cm)", min_value=30.0, max_value=250.0,
