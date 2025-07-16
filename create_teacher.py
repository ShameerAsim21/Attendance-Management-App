from app import create_app, db
from app.models import User, Teacher
from app.utils import hash_password

app = create_app()

with app.app_context():
    user = User(username="teacher1", password=hash_password("admin123"), role="teacher")
    db.session.add(user)
    db.session.flush()

    teacher = Teacher(user_id=user.id, name="Mr. Arham", subject="Computer Science")
    db.session.add(teacher)
    db.session.commit()

    print("✅ Teacher account created: username=teacher1, password=admin123")