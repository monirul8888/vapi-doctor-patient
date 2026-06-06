import streamlit as st
import requests
from datetime import datetime

# -------------------- CONFIG --------------------
API_URL = "https://mop-aged-lining.ngrok-free.dev"

# Page configuration
st.set_page_config(
    page_title="Doctor Appointment System",
    page_icon="🩺",
    layout="wide"
)

# Theme colors
PRIMARY_COLOR = "#4B8BBE"
SECONDARY_COLOR = "#306998"
SUCCESS_COLOR = "#4CAF50"
ERROR_COLOR = "#F44336"

# Sidebar menu
st.sidebar.title("Menu")
menu = ["Schedule Appointment", "Cancel Appointment", "List Appointments", "Search Appointment"]
choice = st.sidebar.radio("Select Action", menu)

st.markdown(f"<h1 style='color:{PRIMARY_COLOR};'>Hospital Appointment System</h1>", unsafe_allow_html=True)
st.markdown("---")

# -------------------- SCHEDULE --------------------
if choice == "Schedule Appointment":
    st.subheader("📝 Schedule a New Appointment")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("Patient Name", placeholder="John Doe")
        with col2:
            reason = st.text_input("Reason for Appointment", placeholder="Routine Checkup")

        start_time = st.text_input("Start Time (YYYY-MM-DD HH:MM)", placeholder="2026-06-07 09:00")

    if st.button("Schedule", key="schedule"):
        try:
            dt_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            payload = {
                "patient_name": patient_name,
                "reason": reason,
                "start_time": dt_obj.isoformat()
            }
            resp = requests.post(f"{API_URL}/schedule_appointment/", json=payload)
            if resp.status_code == 200:
                st.success(f"✅ Appointment scheduled! ID: {resp.json()['id']}")
            else:
                st.error(f"❌ {resp.json()['detail']}")
        except Exception as e:
            st.error(f"❌ {str(e)}")

# -------------------- CANCEL --------------------
elif choice == "Cancel Appointment":
    st.subheader("❌ Cancel Appointment")
    patient_name = st.text_input("Patient Name", placeholder="John Doe", key="cancel_name")
    date = st.date_input("Appointment Date")

    if st.button("Cancel", key="cancel"):
        payload = {"patient_name": patient_name, "date": date.isoformat()}
        resp = requests.post(f"{API_URL}/cancel_appointment/", json=payload)
        if resp.status_code == 200:
            st.success(f"✅ Canceled {resp.json()['canceled_count']} appointment(s)")
        else:
            st.error(f"❌ {resp.json()['detail']}")

# -------------------- LIST --------------------
elif choice == "List Appointments":
    st.subheader("📅 List Appointments by Date")
    date = st.date_input("Select Date", key="list_date")

    if st.button("List", key="list_btn"):
        resp = requests.post(f"{API_URL}/list_appointments/", json={"date": date.isoformat()})
        if resp.status_code == 200:
            data = resp.json()
            if data:
                for a in data:
                    st.markdown(
                        f"""
                        <div style="border-left: 4px solid {PRIMARY_COLOR}; padding: 10px; margin:5px 0; background:#f9f9f9; border-radius:5px;">
                            <strong>ID:</strong> {a['id']}<br>
                            <strong>Patient:</strong> {a['patient_name']}<br>
                            <strong>Reason:</strong> {a['reason']}<br>
                            <strong>Time:</strong> {a['start_time']}<br>
                            <strong>Canceled:</strong> {a['canceled']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("ℹ️ No appointments found for this date")
        else:
            st.error(f"❌ {resp.json()['detail']}")

# -------------------- SEARCH --------------------
elif choice == "Search Appointment":
    st.subheader("🔎 Search Appointment")
    search_type = st.radio("Search by", ["ID", "Patient Name", "Date"])

    if search_type == "ID":
        appointment_id = st.number_input("Appointment ID", min_value=1, step=1, key="search_id")
        if st.button("Search by ID"):
            resp = requests.get(f"{API_URL}/appointments/{appointment_id}")
            if resp.status_code == 200:
                a = resp.json()
                st.markdown(
                    f"<div style='background:#e6f7ff; padding:10px; border-radius:5px;'>"
                    f"<strong>ID:</strong> {a['id']}<br>"
                    f"<strong>Patient:</strong> {a['patient_name']}<br>"
                    f"<strong>Reason:</strong> {a['reason']}<br>"
                    f"<strong>Time:</strong> {a['start_time']}<br>"
                    f"<strong>Canceled:</strong> {a['canceled']}</div>", unsafe_allow_html=True
                )
            else:
                st.error(f"❌ {resp.json()['detail']}")

    elif search_type == "Patient Name":
        patient_name = st.text_input("Patient Name", key="search_patient")
        if st.button("Search by Patient"):
            resp = requests.get(f"{API_URL}/appointments/patient/{patient_name}")
            if resp.status_code == 200:
                data = resp.json()
                for a in data:
                    st.markdown(
                        f"<div style='background:#e6f7ff; padding:10px; border-radius:5px;'>"
                        f"<strong>ID:</strong> {a['id']}<br>"
                        f"<strong>Patient:</strong> {a['patient_name']}<br>"
                        f"<strong>Reason:</strong> {a['reason']}<br>"
                        f"<strong>Time:</strong> {a['start_time']}<br>"
                        f"<strong>Canceled:</strong> {a['canceled']}</div>", unsafe_allow_html=True
                    )
            else:
                st.error(f"❌ {resp.json()['detail']}")

    elif search_type == "Date":
        date = st.date_input("Date", key="search_date")
        if st.button("Search by Date"):
            resp = requests.get(f"{API_URL}/appointments/date/{date}")
            if resp.status_code == 200:
                data = resp.json()
                for a in data:
                    st.markdown(
                        f"<div style='background:#e6f7ff; padding:10px; border-radius:5px;'>"
                        f"<strong>ID:</strong> {a['id']}<br>"
                        f"<strong>Patient:</strong> {a['patient_name']}<br>"
                        f"<strong>Reason:</strong> {a['reason']}<br>"
                        f"<strong>Time:</strong> {a['start_time']}<br>"
                        f"<strong>Canceled:</strong> {a['canceled']}</div>", unsafe_allow_html=True
                    )
            else:
                st.error(f"❌ {resp.json()['detail']}")