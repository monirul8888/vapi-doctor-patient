import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:4444"

st.title("Doctor Appointment System")

menu = ["Schedule Appointment", "Cancel Appointment", "List Appointments", "Get Appointment by ID"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- Schedule Appointment ----------------
if choice == "Schedule Appointment":
    st.header("Schedule a New Appointment")
    patient_name = st.text_input("Patient Name")
    reason = st.text_input("Reason")
    start_time = st.text_input("Start Time (YYYY-MM-DD HH:MM)")

    if st.button("Schedule"):
        try:
            dt_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            payload = {
                "patient_name": patient_name,
                "reason": reason,
                "start_time": dt_obj.isoformat()
            }
            resp = requests.post(f"{API_URL}/schedule_appointment/", json=payload)
            if resp.status_code == 200:
                st.success(f"Appointment scheduled! ID: {resp.json()['id']}")
            else:
                st.error(resp.json()["detail"])
        except Exception as e:
            st.error(str(e))

# ---------------- Cancel Appointment ----------------
elif choice == "Cancel Appointment":
    st.header("Cancel Appointment")
    patient_name = st.text_input("Patient Name")
    date = st.date_input("Appointment Date")

    if st.button("Cancel"):
        payload = {
            "patient_name": patient_name,
            "date": date.isoformat()
        }
        resp = requests.post(f"{API_URL}/cancel_appointment/", json=payload)
        if resp.status_code == 200:
            st.success(f"Canceled {resp.json()['canceled_count']} appointment(s)")
        else:
            st.error(resp.json()["detail"])

# ---------------- List Appointments ----------------
elif choice == "List Appointments":
    st.header("List Appointments by Date")
    date = st.date_input("Select Date")

    if st.button("List"):
        resp = requests.post(f"{API_URL}/list_appointments/", json={"date": date.isoformat()})
        if resp.status_code == 200:
            data = resp.json()
            if data:
                for a in data:
                    st.write(f"ID: {a['id']} | Patient: {a['patient_name']} | Reason: {a['reason']} | Time: {a['start_time']} | Canceled: {a['canceled']}")
            else:
                st.info("No appointments found for this date")
        else:
            st.error(resp.json()["detail"])

# ---------------- Get Appointment by ID ----------------
elif choice == "Get Appointment by ID":
    st.header("Get Appointment by ID")
    appointment_id = st.number_input("Appointment ID", min_value=1, step=1)

    if st.button("Get"):
        resp = requests.get(f"{API_URL}/appointments/{appointment_id}")
        if resp.status_code == 200:
            a = resp.json()
            st.write(f"ID: {a['id']}")
            st.write(f"Patient: {a['patient_name']}")
            st.write(f"Reason: {a['reason']}")
            st.write(f"Time: {a['start_time']}")
            st.write(f"Canceled: {a['canceled']}")
        else:
            st.error(resp.json()["detail"])