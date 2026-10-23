import streamlit as st
from auth import supabase
import datetime

def run_secure_history():
    st.subheader("📋 Secure Clinical History - Private to You")
    
    patient_name = st.text_input("Patient Name")
    age = st.number_input("Age", 1, 120, 25)
    history_text = st.text_area("Clinical History", height=200)

    if st.button("💾 Save Securely", type="primary"):
        if patient_name and history_text:
            try:
                supabase.table("user_data").insert({
                    "user_id": st.session_state.user.id,
                    "tool_name": "Clinical History",
                    "data": {
                        "patient_name": patient_name,
                        "age": age,
                        "history": history_text,
                        "date": str(datetime.datetime.now())
                    }
                }).execute()
                st.success(f"✅ Saved! {patient_name} is secured - only you can see.")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Fill name and history first")

    st.divider()
    st.subheader("Your Saved Patients (Private)")
    try:
        res = supabase.table("user_data").select("*").eq("user_id", st.session_state.user.id).eq("tool_name", "Clinical History").order("created_at", desc=True).execute()
        if res.data:
            for row in res.data:
                d = row['data']
                with st.expander(f"{d.get('patient_name')} - {d.get('age')}y"):
                    st.write(d.get('history'))
                    st.caption(d.get('date'))
        else:
            st.info("No patients yet")
    except Exception as e:
        st.info(f"Loading... {e}")
