from flask import Flask, render_template # import de flask qui est un framework pour un rendu d'une page web
import sqlite3 # import sqlite3 pour l'accès à la base de données
import os # import os pour l'accès à la base de données avec un chemin

app = Flask(__name__) # création d'un objet Flask 

def connect_to_database(): # connexion à la base de données
    conn = sqlite3.connect('carnet_adresses.db')
    cursor = conn.cursor() # création d'un objet cursor qui peremt de récupérer les données de la base de données
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            email TEXT,
            telephone TEXT
        )
    ''') # création d'une table contacts si n'existe pas
    conn.commit() # enregistrement de la table contacts
    return conn # connexion à la base de données

def check_table_exists(): # verifie si la table contacts existe déjà
    if not os.path.isfile('carnet_adresses.db'): # verifie si la base de données existe déjà
        conn = connect_to_database() # connexion à la base de données
        cursor = conn.cursor() # création d'un objet cursor qui permet de récupérer les donné
        cursor.execute('''
            INSERT INTO contacts (nom, prenom, email, telephone)
            VALUES
                ('Doe', 'John', 'feuerfe@gmail.com', '0754242350'),
                ('Smith', 'Jane', 'viheti@gmail.com', '0658472536'),
                ('Doe', 'Alice', 'alice@example.com', '1234567890'),
                ('Johnson', 'David', 'david@example.com', '9876543210'),
                ('Brown', 'Emily', 'emily@example.com', '4567890123'),
                ('Garcia', 'Michael', 'michael@example.com', '7890123456'),
                ('Martinez', 'Olivia', 'olivia@example.com', '2345678901'),
                ('Lee', 'Sophia', 'sophia@example.com', '5678901234'),
                ('Nguyen', 'Daniel', 'daniel@example.com', '8901234567'),
                ('Kim', 'Grace', 'grace@example.com', '0123456789')
        ''') # insertion de nouveaux contacts
        conn.commit() # enregistrement de la table contacts
        conn.close() # fermeture de la connexion à la base de données

@app.route('/') 
def index():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    return render_template('annuaire.html', entries=contacts)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_contact():
    return "Page d'ajout d'un nouveau contact"

@app.route('/modifier', methods=['GET', 'POST'])
def modifier_contact():
    return "Page de modification d'un contact"

@app.route('/supprimer', methods=['GET', 'POST'])
def supprimer_contact():
    return "Page de suppression d'un contact"

@app.route('/contact_details/<int:contact_id>', methods=['GET'])
def contact_details(contact_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id =?', (contact_id,))
    detail = cursor.fetchone()
    conn.close()
    return render_template('detail.html', entries=[detail])

if __name__ == '__main__':
    check_table_exists()
    app.run(debug=True)
