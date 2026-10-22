import streamlit as st
from datetime import date

st.set_page_config(page_title="MediTools", layout="wide")
st.title("MediTools - History Taking")
st.write("Made by fazleazeem71-spec | For Ward Use")

with st.form("hx"):
    st.subheader("1. Bio Data")
    c1,c2,c3 = st.columns(3)
    with c1:
        name = st.text_input("Name")
        sex = st.selectbox("Sex", ["Male","Female"])
        if sex == "Male":
            lab = "Father Name"
        else:
            lab = "Husband Name (Father if unmarried)"
        fh = st.text_input(lab)
    with c2:
        age = st.number_input("Age", 1, 100)
        address = st.text_input("Address")
        job = st.text_input("Occupation")
    with c3:
        mode = st.selectbox("Mode", ["OPD","IPD","ER"])
        d = st.date_input("Date", date.today())
        bed = st.text_input("Ward/Bed")
    st.subheader("2. History")
    comp = st.text_area("Chief Complaint")
    submitted = st.form_submit_button("Generate History")

if submitted:
    st.success(f"Patient: {name}, {sex}, {lab}: {fh}, Age: {age}")
