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
                            url TEXT, reference TEXT, agency TEXT,
                            loyer INTEGER, surface REAL,
                            statut TEXT, derniere_modification TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            action TEXT, appartement_id INTEGER,
                            date TEXT, details TEXT)''')
    conn.close()

@app.route('/add_apartment', methods=['POST'])
def add_apartment():
    data = request.json
    conn = get_db_connection()
    conn.execute('''INSERT INTO appartements (url, reference, agency, loyer, surface, statut, derniere_modification)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))''',
                 (data['url'], data['reference'], data['agency'], data['loyer'], data['surface'], 'en_attente'))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Appartement ajouté avec succès'})

@app.route('/get_apartments', methods=['GET'])
def get_apartments():
    conn = get_db_connection()
    appartements = conn.execute('SELECT * FROM appartements').fetchall()
    conn.close()
    return jsonify([dict(appartement) for appartement in appartements])

@app.route('/update_status/<int:id>', methods=['PUT'])
def update_status(id):
    statut = request.json['statut']
    conn = get_db_connection()
    conn.execute('UPDATE appartements SET statut = ?, derniere_modification = datetime("now") WHERE id = ?', 
                 (statut, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Statut mis à jour'})

@app.route('/delete_apartment/<int:id>', methods=['DELETE'])
def delete_apartment(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM appartements WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Appartement supprimé'})

@app.route('/logs', methods=['GET'])
def get_logs():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM logs').fetchall()
    conn.close()
    return jsonify([dict(log) for log in logs])

@app.route('/export_csv', methods=['GET'])
def export_csv():
    try:
        conn = get_db_connection()
        appartements = conn.execute('SELECT * FROM appartements').fetchall()
        conn.close()

        with open('appartements.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'URL', 'Référence', 'Agence', 'Loyer', 'Surface', 'Statut', 'Dernière Modification'])
            for appartement in appartements:
                writer.writerow([appartement['id'], appartement['url'], appartement['reference'],
                                 appartement['agency'], appartement['loyer'], appartement['surface'],
                                 appartement['statut'], appartement['derniere_modification']])
        return jsonify({'message': 'Export réussi !'})
    except Exception as e:
        return jsonify({'error': f'Une erreur est survenue lors de l\'exportation : {str(e)}'}), 500

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000)
