import sqlite3

conn = sqlite3.connect('appartements.db')
c = conn.cursor()

# Créer les tables
c.execute('''CREATE TABLE IF NOT EXISTS appartements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT, nom TEXT, adresse TEXT,
                loyer INTEGER, surface REAL,
                statut TEXT, derniere_modification TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT, appartement_id INTEGER,
                date TEXT, details TEXT)''')

conn.commit()
conn.close()
