
from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Student, Teacher, Attendance
from app import db, login_manager, socketio
from datetime import date
from app.utils import *

bp = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password(data['password'], user.password):
        login_user(user)
        return jsonify({'status': 'success', 'role': user.role})
    return jsonify({'status': 'fail'}), 401

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'logged out'})

@bp.route('/student/mark', methods=['POST'])
@login_required
def student_mark_attendance():
    method = request.json['method']
    student = current_user.student
    success = False

    if method == 'face':
        cap = cv2.VideoCapture(0)
        _, frame = cap.read()
        cap.release()
        success = match_face(student.face_encoding, frame)
    elif method == 'qr':
        success = scan_qr(student.roll_number)

    if success:
        new_attendance = Attendance(
            student_id=student.id, date=date.today(), method=method, status='present'
        )
        db.session.add(new_attendance)
        db.session.commit()
        socketio.emit('attendance_update', {'student': student.name})
        return jsonify({'status': 'marked'})
    return jsonify({'status': 'failed'})

@bp.route('/student/stats')
@login_required
def student_stats():
    s = current_user.student
    total = len(s.attendance)
    present = len([a for a in s.attendance if a.status == 'present'])
    return jsonify({'total': total, 'present': present})

@bp.route('/teacher/add_student', methods=['POST'])
@login_required
def teacher_add_student():
    data = request.json
    user = User(
        username=data['username'],
        password=hash_password(data['password']),
        role='student'
    )
    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        name=data['name'],
        roll_number=data['roll_number'],
        class_name=data['class'],
        face_encoding=get_face_encoding(data['image_path'])
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({'status': 'student added'})

@bp.route('/teacher/stats')
@login_required
def teacher_stats():
    all_stats = []
    students = Student.query.all()
    for s in students:
        total = len(s.attendance)
        present = len([a for a in s.attendance if a.status == 'present'])
        all_stats.append({
            'name': s.name,
            'roll_number': s.roll_number,
            'present': present,
            'total': total
        })
    return jsonify(all_stats)
