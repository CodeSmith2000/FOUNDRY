#  ----------------------------------------------------------------------------
#  FOUNDRY SYSTEMS // SOURCE CODE
#  Copyright (c) 2026.
#  
#  Use of this source code is governed by the Foundry Source License (FSL) v1.0.
#  
#  ALLOWED:   Personal use, Internal Business use, Consulting/Installation services, Free Redistribution.
#  FORBIDDEN: Selling the binary, hosting as a SaaS for others, removing Trademarks.
#  ----------------------------------------------------------------------------

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = 'projects_vault.db'

def init_db():
    """Initializes the SQLite database with the core schema if it doesn't exist."""
    if not os.path.exists(DB_PATH):
        print("Initializing FOUNDRY_VAULT database...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create Projects Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Parts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                part_num TEXT,
                part_hash TEXT,
                req INTEGER DEFAULT 0,
                stock INTEGER DEFAULT 0,
                cost REAL DEFAULT 0.0,
                bulk_qty INTEGER DEFAULT 1,
                lead_time TEXT,
                img TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database engine online.")

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/get_db')
def get_db():
    """Returns the database file as a binary blob for sql.js."""
    if not os.path.exists(DB_PATH):
        init_db()
    return send_from_directory('.', DB_PATH)

@app.route('/upload_db', methods=['POST'])
def upload_db():
    """Persists the binary blob sent from the browser to the local disk."""
    try:
        data = request.get_data()
        with open(DB_PATH, 'wb') as f:
            f.write(data)
        return jsonify({"status": "FOUNDRY_SYNC_COMPLETE"}), 200
    except Exception as e:
        return jsonify({"status": "SYNC_ERROR", "error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    # Using port 8000 to match the README instructions
    print("FOUNDRY Terminal accessible at http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=False)
