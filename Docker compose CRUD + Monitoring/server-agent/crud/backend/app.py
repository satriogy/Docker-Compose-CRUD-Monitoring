from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Konfigurasi database PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@postgres:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Pastikan folder uploads ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# Model untuk menyimpan data file
class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)

# Fungsi untuk memeriksa ekstensi file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route untuk halaman utama
@app.route('/')
def home():
    return '''
    <!doctype html>
    <title>Home</title>
    <h1>Welcome to the File Upload Service</h1>
    <ul>
        <li><a href="/upload_form">Upload File</a></li>
        <li><a href="/uploads">List Uploaded Files</a></li>
    </ul>
    '''

# Route untuk mengunggah file melalui browser
@app.route('/upload_form', methods=['GET'])
def upload_form():
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload File</h1>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

# Route untuk meng-upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Simpan detail file ke database
        new_file = FileUpload(filename=filename)
        db.session.add(new_file)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    return jsonify({'message': 'Invalid file type'}), 400

# Route untuk menampilkan file
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    # Cari file berdasarkan ID
    file_to_delete = FileUpload.query.get(file_id)
    if not file_to_delete:
        return jsonify({'message': 'File not found'}), 404

    # Hapus file dari sistem
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_to_delete.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    # Hapus data dari database
    db.session.delete(file_to_delete)
    db.session.commit()

    return jsonify({'message': 'File deleted successfully'}), 200


# Route untuk menampilkan daftar file yang telah di-upload
@app.route('/uploads', methods=['GET'])
def list_uploaded_files():
    files = FileUpload.query.all()
    html_content = '''
    <!doctype html>
    <title>Uploaded Files</title>
    <h1>Uploaded Files</h1>
    <ul>
    '''
    for file in files:
        html_content += f'''
        <li>
            <p>ID: {file.id}</p>
            <p>Filename: {file.filename}</p>
            <img src="/uploads/{file.filename}" alt="{file.filename}" style="max-width: 200px; height: auto;">
            <form method="POST" action="/delete/{file.id}" style="display:inline;">
                <button type="submit">Delete</button>
            </form>
        </li>
        '''
    html_content += '</ul>'
    return html_content

if __name__ == '__main__':
    db.create_all()  # Membuat tabel di database
    app.run(host='0.0.0.0', port=5000, debug=True)
