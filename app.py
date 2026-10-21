import streamlit as st
from datetime import date

st.set_page_config(page_title="MediTools", page_icon="🩺")
st.title("🩺 MediTools - History Taking")
st.write("Made by fazleazeem71-spec | For Ward Use")

with st.form("hx"):
    st.subheader("1. Bio Data")
    c1,c2,c3 = st.columns(3)
    with c1:
        name = st.text_input("Name")
        fname = st.text_input("F/H Name")
        sex = st.selectbox("Sex", ["Male","Female"])
    with c2:
        age = st.number_input("Age", 1, 100, 25)
        address = st.text_input("Address")
        occupation = st.text_input("Occupation")
    with c3:
        mode = st.selectbox("Mode", ["OPD","Emergency"])
        date_adm = st.date_input("Date", date.today())
        bed = st.text_input("Ward/Bed")
    
    st.subheader("2. History")
    chief = st.text_area("Chief Complaints")
    hopi = st.text_area("HOPI")
    past_med = st.text_input("Past Medical Hx")
    past_surg = st.text_input("Past Surgical Hx")
    drug_hx = st.text_input("Drug Hx")
    allergic = st.text_input("Allergic Hx")
    family = st.text_input("Family Hx")
    transf = st.text_input("Transfusion Hx")
    personal = st.text_input("Personal Hx")
    travel = st.text_input("Travel Hx")
    socio = st.text_input("Socioeconomic Hx")
    mens = st.text_input("Menstrual/Obstetric Hx")
    ros = st.text_input("Immunization & ROS")
    
    btn = st.form_submit_button("GENERATE SHEET")

if btn:
    sheet = f"""
Name: {name} S/O {fname} | {age}/{sex}
Address: {address} | {occupation}
Admission: {mode} on {date_adm} | {bed}
C/C: {chief}
HOPI: {hopi}
Past Med: {past_med} | Surg: {past_surg}
Drug: {drug_hx} | Allergic: {allergic}
Family: {family} | Transfusion: {transf}
Personal: {personal} | Travel: {travel}
Socio: {socio} | Mens: {mens} | ROS: {ros}
"""
    st.code(sheet)
    st.download_button("📥 Download Sheet", sheet, f"{name}.txt")
    st.balloons()
    st.success("Ready to share!")
