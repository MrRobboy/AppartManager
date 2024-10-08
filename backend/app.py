from flask import Flask, request, jsonify
import sqlite3
import csv

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('appartements.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS appartements (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ville TEXT, nom TEXT, adresse TEXT,
                            loyer INTEGER, surface REAL,
                            agence TEXT, url_annonce TEXT,
                            statut TEXT, derniere_modification TEXT)''')
    conn.close()

@app.route('/add_apartment', methods=['POST'])
def add_apartment():
    data = request.json
    # En supposant que les champs nom, adresse et statut sont fournis
    conn = get_db_connection()
    conn.execute('''INSERT INTO appartements (ville, nom, adresse, loyer, surface, agence, url_annonce, statut, derniere_modification)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))''',
                 (data['ville'], data['nom'], data['adresse'], data['loyer'], data['surface'], data['agence'], data['url_annonce'], 'en_attente'))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Appartement ajouté avec succès'})

@app.route('/get_apartments', methods=['GET'])
def get_apartments():
    conn = get_db_connection()
    appartements = conn.execute('SELECT * FROM appartements').fetchall()
    conn.close()
    return jsonify([dict(appartement) for appartement in appartements])

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000)
