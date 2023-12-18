# Importation des modules nécessaires
from flask import Flask, render_template, request, redirect, url_for # Import de Flask pour la création d'une application web
import sqlite3 # Import de sqlite3 pour interagir avec la base de données
import os # Import du module os pour les opérations système

# Initialisation de l'application Flask
app = Flask(__name__) 

# Fonction pour établir la connexion à la base de données
def connect_to_database(): # connexion à la base de données
    conn = sqlite3.connect('../Projet_Python/carnet_adresses.db')
    cursor = conn.cursor() # Création d'un objet cursor pour exécuter des requêtes SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            email TEXT,
            telephone TEXT
        )
    ''') # Création d'une table "contacts" si elle n'existe pas
    
    conn.commit() # Enregistrement des modifications
    return conn # Retourne l'objet de connexion à la base de données

# Fonction pour vérifier si la table existe, sinon l'initialise avec des données fictives
def check_table_exists(): # Vérification de l'existence de la base de données
    if not os.path.isfile('../Projet_Python/carnet_adresses.db'): # verifie si la base de données existe déjà
        conn = connect_to_database() # Établissement de la connexion à la base de données
        cursor = conn.cursor() # Création d'un objet cursor pour exécuter des requêtes SQL
        cursor.executemany('''
            INSERT INTO contacts (nom, prenom, email, telephone)
            VALUES (?, ?, ?, ?)
        ''', [
                ('Doe', 'John', 'john@gmail.com', '0754242350'),
                ('Smith', 'Jane', 'jane@gmail.com', '0658472536'),
                ('Johnson', 'David', 'david@gmail.com', '9876543210'),
                ('Brown', 'Emily', 'emily@gmail.com', '4567890123'),
                ('Garcia', 'Michael', 'michael@gmail.com', '7890123456'),
                ('Martinez', 'Olivia', 'olivia@gmail.com', '2345678901'),
                ('Lee', 'Sophia', 'sophia@gmail.com', '5678901234'),
                ('Nguyen', 'Daniel', 'daniel@gmail.com', '8901234567'),
                ('Kim', 'Grace', 'grace@gmail.com', '0123456789'),
                ('Wilson', 'Liam', 'liam@gmail.com', '6745238901'),
                ('Anderson', 'Ella', 'ella@gmail.com', '7856349012'),
                ('Thomas', 'Ava', 'ava@gmail.com', '9012873456'),
                ('Jackson', 'Noah', 'noah@gmail.com', '1234567890'),
                ('White', 'Mia', 'mia@gmail.com', '9876543210'),
                ('Harris', 'James', 'james@gmail.com', '5678901234'),
                ('Clark', 'Evelyn', 'evelyn@gmail.com', '2345678901'),
                ('Lewis', 'Harper', 'harper@gmail.com', '3456789012'),
                ('Hill', 'Charlotte', 'charlotte@gmail.com', '4567890123'),
                ('Young', 'William', 'william@gmail.com', '5678901234'),
                ('Scott', 'Amelia', 'amelia@gmail.com', '6789012345'),
                ('Adams', 'Oliver', 'oliver@gmail.com', '7890123456'),
                ('Allen', 'Sophie', 'sophie@gmail.com', '8901234567'),
                ('Green', 'Lucas', 'lucas@gmail.com', '0123456789'),
                ('Hughes', 'Isabella', 'isabella@gmail.com', '1234567890'),
                ('Carter', 'Ethan', 'ethan@gmail.com', '2345678901'),
                ('Morris', 'Aria', 'aria@gmail.com', '3456789012'),
                ('Parker', 'Alexander', 'alexander@gmail.com', '4567890123'),
                ('Turner', 'Scarlett', 'scarlett@gmail.com', '5678901234'),
                ('Cooper', 'Grace', 'grace1@gmail.com', '6789012345'),
                ('Murphy', 'Hannah', 'hannah@gmail.com', '7890123456'),
                ('Hayes', 'Lily', 'lily@gmail.com', '8901234567'),
                ('Morgan', 'Ethan', 'ethan1@gmail.com', '0123456789'),
                ('Ross', 'Aiden', 'aiden@gmail.com', '1234567890'),
                ('Russell', 'Chloe', 'chloe@gmail.com', '2345678901'),
                ('Long', 'Jacob', 'jacob@gmail.com', '3456789012'),
                ('Bell', 'Zoe', 'zoe@gmail.com', '4567890123'),
                ('Sanders', 'Madison', 'madison@gmail.com', '5678901234'),
                ('Reed', 'Avery', 'avery@gmail.com', '6789012345'),
                ('Griffin', 'Ella', 'ella1@gmail.com', '7890123456'),
                ('Grant', 'Logan', 'logan@gmail.com', '8901234567'),
                ('Lane', 'Grace', 'grace2@gmail.com', '0123456789'),
                ('Watson', 'Layla', 'layla@gmail.com', '1234567890'),
                ('Murray', 'Michael', 'michael1@gmail.com', '2345678901'),
                ('Perry', 'Liam', 'liam1@gmail.com', '3456789012'),
                ('Rose', 'Mia', 'mia1@gmail.com', '4567890123'),
                ('Cox', 'Harper', 'harper1@gmail.com', '5678901234'),
                ('Bishop', 'Emma', 'emma@gmail.com', '6789012345'),
        ]) # insertion de nouveaux contacts
        conn.commit() # Enregistrement des modifications
        conn.close() # Fermeture de la connexion à la base de données

# Route pour la page d'accueil affichant tous les contacts
@app.route('/', methods=['GET', 'POST']) 
def index():
    conn = connect_to_database() # Établissement de la connexion à la base de données
    cursor = conn.cursor() # Création d'un objet cursor pour exécuter des requêtes SQL
    cursor.execute('SELECT * FROM contacts')  # Récupération de tous les contacts de la table "contacts"
    contacts = cursor.fetchall() # Récupération des résultats
    conn.close() # Fermeture de la connexion à la base de données
    return render_template('annuaire.html', entries=contacts) # Affichage des contacts sur la page web

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_contact():
    if request.method == 'POST': # Vérifie si le formulaire a été envoyé
        nom = request.form['nom'] # Récupération du nom
        prenom = request.form['prenom'] # Récupération du prénom
        email = request.form['email'] # Récupération du email
        telephone = request.form['telephone'] # Récupération du numéro de téléphone
        
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts WHERE telephone=?', (telephone,))
        telephone_existe = cursor.fetchone()
        
        if telephone_existe: # Vérifie si le numéro de téléphone existe déjà
            return "Le numéro de téléphone existe déjà. Veuillez réessayer."
        
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts WHERE email=?', (email,))
        email_existe = cursor.fetchone()
        
        if email_existe: # Vérifie si le numéro de téléphone existe déjà
            return "L'adresse e-mail existe déjà. Veuillez réessayer."

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (nom, prenom, email, telephone) VALUES (?, ?, ?, ?)',
                       (nom, prenom, email, telephone)) # Enregistrement du nouveau contact
        conn.commit()
        conn.close()

        return redirect(url_for('index')) # Redirection vers la page d'accueil

    return render_template('ajout.html') # Affichage de la page ajout

# Route pour la page de contact à modifier
@app.route('/modifier_contact/<int:contact_id>', methods=['GET', 'POST']) 
def modifier_contact(contact_id):
    if request.method == 'POST': # Vérifie si le formulaire a été envoyé
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        telephone = request.form['telephone']
        
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('UPDATE contacts SET nom =?, prenom =?, email =?, telephone =? WHERE id =?',
                       (nom, prenom, email, telephone, contact_id)) # Modification du nouveau contact
        conn.commit()
        conn.close()
        
        return redirect(url_for('index')) # Redirection vers la page d'accueil
    
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id =?', (contact_id,)) # Récupération du contact à modifier
    modifie = cursor.fetchone()
    conn.close()
    return render_template('modifier_contact.html', modifie=[modifie]) # Affichage du contact à modifier

# Route pour la page de suppression d'un contact
@app.route('/supprimer/<int:contact_id>', methods=['GET', 'POST'])
def supprimer(contact_id): 
    if request.method == 'GET': # Vérifie si le formulaire a été envoyé
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE id =?', (contact_id,)) # Suppression du contact
        conn.commit()
        conn.close()
        return redirect(url_for('index')) # Redirection vers la page d'accueil
    else:
        pass # Rien faire

# Route pour la page de details d'un contact
@app.route('/contact_details/<int:contact_id>', methods=['GET'])
def contact_details(contact_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id =?', (contact_id,)) # Récupération du détail de contact 
    detail = cursor.fetchone()
    conn.close()
    return render_template('detail.html', detail=[detail]) # Rédirection vers la page details

# Route pour la recherche d'un contact
@app.route('/rechercher', methods=['GET'])
def rechercher_contact():
    terme_recherche = request.args.get('search', '')  # Récupère le terme de recherche depuis l'URL
    
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE nom LIKE ? OR prenom LIKE ? OR email LIKE ?",
                   ('%' + terme_recherche + '%', '%' + terme_recherche + '%', '%' + terme_recherche + '%')) # Récupération de tous les contacts qui contiennent le terme recherche
    contacts = cursor.fetchall()
    conn.close()

    return render_template('annuaire.html', entries=contacts) # Redirection vers la page annuaire

# Route pour la page de tri des contacts
@app.route('/tri_contacts', methods=['GET'])
def tri_contacts():
    champ = request.args.get('champ') # Récupère le champ de tri
    sens = request.args.get('sens') # Récupère le sens de tri
    conn = connect_to_database()
    cursor = conn.cursor()
    query = f"SELECT * FROM contacts ORDER BY {champ} {sens}" # Récupération de tous les contacts de l'orde du sens de tri et le champ de tri
    cursor.execute(query)
    tries = cursor.fetchall()
    conn.close()
    
    return render_template('annuaire.html', entries=tries) # Redirection vers la page annuaire


if __name__ == '__main__':
    check_table_exists()
    app.run(debug=True)
