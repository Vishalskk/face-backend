from flask import Flask, request, jsonify
import face_recognition
import os

app = Flask(__name__)
EVENT_DIR = "event_photos"

@app.route('/find-matches', methods=['POST'])
def find_matches():
    user_file = request.files['user_image']
    event = request.form['event']
    user_image = face_recognition.load_image_file(user_file)
    user_enc = face_recognition.face_encodings(user_image)[0]
    
    matched = []
    folder = os.path.join(EVENT_DIR, event)
    for fname in os.listdir(folder):
        img_path = os.path.join(folder, fname)
        img = face_recognition.load_image_file(img_path)
        encs = face_recognition.face_encodings(img)
        for enc in encs:
            if face_recognition.compare_faces([user_enc], enc)[0]:
                matched.append(fname)
                break
    return jsonify({'matched_files': matched})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
v
