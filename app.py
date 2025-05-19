from flask import Flask, request, jsonify, send_from_directory
import os
import face_recognition
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "event_photos"
MATCHED_FOLDER = "matched_photos"
os.makedirs(MATCHED_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    user_image = face_recognition.load_image_file(file)
    user_encoding = face_recognition.face_encodings(user_image)[0]

    matched_files = []

    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(UPLOAD_FOLDER, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            for encoding in encodings:
                result = face_recognition.compare_faces([user_encoding], encoding)
                if result[0]:
                    matched_files.append(filename)
                    break

    # Optional: copy matched to a folder for download
    for filename in matched_files:
        src = os.path.join(UPLOAD_FOLDER, filename)
        dst = os.path.join(MATCHED_FOLDER, filename)
        if not os.path.exists(dst):
            os.system(f"cp \"{src}\" \"{dst}\"")

    return jsonify({"matched_images": matched_files})

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(MATCHED_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
v
