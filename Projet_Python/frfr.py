import sqlite3

conn = sqlite3.connect('carnet_adresses.db')
cursor = conn.cursor()

# Exécutez une requête SELECT pour récupérer toutes les lignes de la table 'contacts'
cursor.execute('SELECT * FROM contacts')
rows = cursor.fetchall()

# Affichez les données récupérées dans la console
for row in rows:
    print(row)

# Fermez la connexion à la base de données
conn.close()