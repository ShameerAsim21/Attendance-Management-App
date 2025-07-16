
import face_recognition
import cv2
import qrcode
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(pw): return generate_password_hash(pw)
def check_password(pw, hashed): return check_password_hash(hashed, pw)

def get_face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None

def match_face(known, frame):
    rgb = frame[:, :, ::-1]
    enc = face_recognition.face_encodings(rgb)
    return face_recognition.compare_faces([known], enc[0])[0] if enc else False

def generate_qr(data, filename='qr.png'):
    img = qrcode.make(data)
    img.save(filename)

def scan_qr(expected):
    cap = cv2.VideoCapture(0)
    qr = cv2.QRCodeDetector()
    while True:
        _, frame = cap.read()
        data, bbox, _ = qr.detectAndDecode(frame)
        if data:
            cap.release()
            return data == expected
