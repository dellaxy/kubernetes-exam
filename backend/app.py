from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
MAX_FILE_SIZE = os.environ.get('MAX_FILE_SIZE')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= int(MAX_FILE_SIZE)


@app.route('/upload', methods=['POST'])  # Remove '/api' prefix
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
        images = []
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                with open(file_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    images.append({
                        'filename': filename,
                        'data': encoded_string
                    })
        return jsonify({'images': images}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Add host binding