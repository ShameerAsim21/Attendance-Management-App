import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Teacher Dashboard", page_icon="🧑‍🏫")
st.title("🧑‍🏫 Teacher Attendance Dashboard")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Teacher Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        if res.status_code == 200 and res.json().get('role') == 'teacher':
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid credentials or role.")
else:
    st.sidebar.success("👨‍🏫 Logged in as Teacher")

    st.subheader("➕ Add New Student")
    with st.form("add_student_form"):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        name = st.text_input("Full Name")
        roll = st.text_input("Roll Number")
        cls = st.text_input("Class")
        img_path = st.text_input("Face Image Path (absolute path)")
        submitted = st.form_submit_button("Add Student")
        if submitted:
            res = requests.post(f"{BASE_URL}/teacher/add_student", json={
                "username": uname,
                "password": pwd,
                "name": name,
                "roll_number": roll,
                "class": cls,
                "image_path": img_path
            })
            if res.status_code == 200:
                st.success("✅ Student added.")
            else:
                st.error("❌ Failed to add student.")

    st.subheader("📈 Attendance Overview")
    res = requests.get(f"{BASE_URL}/teacher/stats")
    if res.status_code == 200:
        for s in res.json():
            st.write(f"👤 {s['name']} ({s['roll_number']})")
            st.progress(s['present'] / s['total'] if s['total'] > 0 else 0)
    else:
        st.warning("⚠️ Unable to fetch attendance stats")

    if st.button("Logout"):
        requests.get(f"{BASE_URL}/logout")
        st.session_state.logged_in = False
        st.rerun()
# run using: python -m streamlit run streamlit_gui/teacher_gui.py