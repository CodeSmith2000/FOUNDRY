from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import sqlite3

app = Flask(__name__)
CORS(app)

VAULT_DB = 'projects_vault.db'
SALES_DB = 'sales_command.db'

def init_dbs():
    # We DO NOT initialize the Vault DB here anymore. 
    # The frontend JavaScript handles the creation of projects_vault.db.
    
    # Initialize Sales (Orders) ONLY
    conn = sqlite3.connect(SALES_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        project_id TEXT, 
        hash TEXT, 
        customer TEXT, 
        address TEXT, 
        qty INTEGER, 
        status TEXT, 
        date TEXT)''')
    conn.commit()
    conn.close()
    print("Sales Database Initialized.")

@app.route('/get_vault')
def get_vault(): 
    # If projects_vault.db doesn't exist yet, this naturally returns a 404, 
    # which triggers your frontend's JS to build the new vault.
    return send_from_directory('.', VAULT_DB)

@app.route('/get_sales')
def get_sales(): 
    return send_from_directory('.', SALES_DB)

@app.route('/save_vault', methods=['POST'])
def save_vault():
    with open(VAULT_DB, 'wb') as f: 
        f.write(request.get_data())
    return jsonify({"status": "VAULT_SAVED"}), 200

@app.route('/save_sales', methods=['POST'])
def save_sales():
    with open(SALES_DB, 'wb') as f: 
        f.write(request.get_data())
    return jsonify({"status": "SALES_SAVED"}), 200

@app.route('/')
def serve_index(): 
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path): 
    return send_from_directory('.', path)

if __name__ == '__main__':
    init_dbs()
    app.run(host='0.0.0.0', port=8000, debug=True)
