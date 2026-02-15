from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) 

# UPDATED FILENAME
DB_FILE = "projects_vault.db"

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/get_db')
def get_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'rb') as f:
            return f.read()
    # Return a 404 if the file isn't there yet so the JS can create a new one
    return jsonify({"error": "No DB found"}), 404

@app.route('/save_db', methods=['POST'])
def save_db():
    data = request.get_data()
    try:
        with open(DB_FILE, 'wb') as f:
            f.write(data)
        return jsonify({"status": "SYNC_COMPLETE", "file": DB_FILE})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

if __name__ == '__main__':
    # Running on 8000
    app.run(port=8000, debug=True)