from flask import Flask, request, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
import time
from datetime import datetime, timedelta

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
EXPIRATION_TIME = 3 * 60 * 60  # 3 jam
ALLOWED_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'gif', 'bmp',       # Gambar
    'mp3', 'mp4', 'wav', 'ogg', 'webm',       # Audio/video
    'pdf', 'doc', 'docx', 'xls', 'xlsx',      # Dokumen
    'txt', 'zip', 'rar'                       # File umum
}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def cleanup_old_files():
    now = time.time()
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(filepath):
            if now - os.path.getmtime(filepath) > EXPIRATION_TIME:
                os.remove(filepath)


@app.route('/', methods=['GET', 'POST'])
def index():
    cleanup_old_files()
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No file part'
        file = request.files['image']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(unique_name))
            file.save(filepath)
            image_url = url_for('uploaded_file', filename=unique_name, _external=True)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({'url': image_url})
            return render_template('index.html', image_url=image_url)
        else:
            return "File tidak diizinkan.", 400

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

