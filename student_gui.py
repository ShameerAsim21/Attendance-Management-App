import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Student Attendance", page_icon="🎓")
st.title("🎓 Student Attendance System")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Student Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        if res.status_code == 200 and res.json().get('role') == 'student':
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid credentials or role.")
else:
    st.sidebar.success("🧑‍🎓 Logged in as Student")

    st.subheader("📍 Mark Attendance")
    method = st.radio("Choose Method", ["Face Recognition", "QR Code"])
    method_api = "face" if method == "Face Recognition" else "qr"

    if st.button("Mark Attendance"):
        res = requests.post(f"{BASE_URL}/student/mark", json={"method": method_api})
        if res.status_code == 200:
            st.success("✅ Attendance marked!")
        else:
            st.error("❌ Failed to mark attendance.")

    st.subheader("📊 Attendance Statistics")
    res = requests.get(f"{BASE_URL}/student/stats")
    if res.status_code == 200:
        data = res.json()
        st.metric("Total Classes", data["total"])
        st.metric("Present", data["present"])
        pct = (data["present"] / data["total"] * 100) if data["total"] > 0 else 0
        st.metric("Attendance %", f"{pct:.2f}%")
        st.progress(pct / 100)
    else:
        st.warning("⚠️ Unable to load stats")

    if st.button("Logout"):
        requests.get(f"{BASE_URL}/logout")
        st.session_state.logged_in = False
        st.rerun()

## run using: python -m streamlit run streamlit_gui/student_gui.py
