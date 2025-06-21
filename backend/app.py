from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
MAX_FILE_SIZE = os.environ.get('MAX_FILE_SIZE')

def allowed_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= int(MAX_FILE_SIZE)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['image']
    if file is None or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file_size(file):
        return jsonify({'error': 'File size exceeds the limit of 10MB'}), 400
    
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return jsonify({'error': 'File type not allowed. Only PNG, JPG, JPEG, and GIF are allowed.'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200


@app.route('/getImages', methods=['GET'])
def get_images():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        return jsonify({'images': images}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500