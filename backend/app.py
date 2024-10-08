from flask import Flask, request, jsonify
import sqlite3
import csv  # Assure-toi d'importer le module csv
from scraping import scrape_apartment_info

app = Flask(__name__)

# Connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('appartements.db')
    conn.row_factory = sqlite3.Row
    return conn

# Création des tables (exécuté au démarrage)
def create_tables():
    conn = get_db_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS appartements (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            url TEXT, nom TEXT, adresse TEXT,
                            loyer INTEGER, surface REAL,
                            statut TEXT, derniere_modification TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            action TEXT, appartement_id INTEGER,
                            date TEXT, details TEXT)''')
    conn.close()

# Route pour ajouter un appartement
@app.route('/add_apartment', methods=['POST'])
def add_apartment():
    data = request.json
    try:
        # Scrape les informations de l'appartement
        info = scrape_apartment_info(data['url'])
        
        # Connexion à la base de données et insertion des données
        conn = get_db_connection()
        conn.execute('''INSERT INTO appartements (url, nom, adresse, loyer, surface, statut, derniere_modification)
                        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))''',
                     (data['url'], info['nom'], info['adresse'], info['loyer'], info['surface'], 'en_attente'))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Appartement ajouté avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Code d'erreur 400 pour les demandes incorrectes

# Route pour modifier le statut d'un appartement
@app.route('/update_status/<int:id>', methods=['PUT'])
def update_status(id):
    statut = request.json['statut']
    conn = get_db_connection()
    conn.execute('UPDATE appartements SET statut = ?, derniere_modification = datetime("now") WHERE id = ?', 
                 (statut, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Statut mis à jour'})

# Route pour supprimer un appartement
@app.route('/delete_apartment/<int:id>', methods=['DELETE'])
def delete_apartment(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM appartements WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Appartement supprimé'})

# Route pour afficher les logs
@app.route('/logs', methods=['GET'])
def get_logs():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM logs').fetchall()
    conn.close()
    return jsonify([dict(log) for log in logs])

# Route pour exporter les données en CSV
@app.route('/export_csv', methods=['GET'])
def export_csv():
    try:
        conn = get_db_connection()
        appartements = conn.execute('SELECT * FROM appartements').fetchall()
        conn.close()

        with open('appartements.csv', 'w', newline='') as f:  # 'newline' pour éviter les lignes vides sous Windows
            writer = csv.writer(f)
            writer.writerow(['ID', 'URL', 'Nom', 'Adresse', 'Loyer', 'Surface', 'Statut', 'Dernière Modification'])
            for appartement in appartements:
                writer.writerow([appartement['id'], appartement['url'], appartement['nom'],
                                 appartement['adresse'], appartement['loyer'], appartement['surface'],
                                 appartement['statut'], appartement['derniere_modification']])
        return jsonify({'message': 'Export réussi !'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Gérer les erreurs

# Démarrer l'application Flask
if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000)
