from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/app/uploads')
MAX_FILE_SIZE = os.environ.get('MAX_FILE_SIZE', '10485760')
DB_HOST = os.environ.get('DB_HOST', 'database-service.exam-richard.svc.cluster.local')
DB_NAME = os.environ.get('DB_NAME', 'exam_db')
DB_USER = os.environ.get('DB_USER', 'exam_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

if UPLOAD_FOLDER:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

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
    
    # Save to database
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO images (filename, file_path) VALUES (%s, %s)",
            (file.filename, file_path)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

@app.route('/getImages', methods=['GET'])
def get_images():
    try:
        # Get image records from database
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, filename, file_path FROM images ORDER BY upload_date DESC")
        db_images = cur.fetchall()
        cur.close()
        conn.close()
        
        images = []
        for record in db_images:
            file_path = record['file_path']
            if os.path.exists(file_path):
                with open(file_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    images.append({
                        'id': record['id'],
                        'filename': record['filename'],
                        'data': encoded_string
                    })
        
        return jsonify({'images': images}), 200
    except Exception as e:
        print(f"Error getting images: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)