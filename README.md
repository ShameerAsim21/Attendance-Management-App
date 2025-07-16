Attendance Management System (AMS)
==================================

This is a Python-based Attendance Management System using:
- Flask (Backend)
- Streamlit (GUI for students and teachers)
- OpenCV & face_recognition (for facial recognition)
- SQLite (for data storage)

----------------------------------
📁 Project Structure:
----------------------------------
attendance_system/
│
├── app/
│   ├── __init__.py         # Initializes Flask app
│   ├── models.py           # SQLAlchemy models
│   ├── routes.py           # Flask API endpoints
│   ├── utils.py            # Utility functions
│
├── instance/
│   └── ams.db              # SQLite database (auto-created)
│
├── streamlit_gui/
│   ├── student_gui.py      # Streamlit UI for students
│   ├── teacher_gui.py      # Streamlit UI for teachers
│   └── students_faces/     # Stored student face data
│
├── create_teacher.py       # Script to add a default teacher and user
├── run.py                  # Flask app launcher
├── requirements.txt        # Python dependencies

----------------------------------
✅ Notes:
----------------------------------
- Ensure face images are clear, front-facing, and accessible.
- Student face data is saved in `students_faces/`.
- Database (`ams.db`) is automatically created on first run.
- Run everything from the `attendance_system` root folder.

=================================================
How to Run the Attendance Management System (AMS)
=================================================

Follow these steps to run the backend Flask server and the Streamlit GUI apps.

----------------------------------
📁 Step-by-Step Guide:
----------------------------------

1. Open Command Prompt or VS Code terminal.

2. Navigate to the project folder:

3. Install all required packages:

4. If there is a database error, delete the old database:

5. Run the Flask backend server:

7. In a new terminal window, run the Streamlit GUI for teachers and students:
    teachers: python -m streamlit run streamlit_gui/teacher_gui.py
    students: python -m streamlit run streamlit_gui/student_gui.py

Notes:
----------------------------------
- Make sure images used for face recognition are clear and valid.
- Run all commands from the root folder (attendance_system).
- Run backend before launching Streamlit apps to avoid connection errors.


Code by: Muhammad Shameer Asim
