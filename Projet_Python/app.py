from flask import Flask, render_template, request, redirect, url_for # import de flask qui est un framework pour un rendu d'une page web
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

@app.route('/', methods=['GET', 'POST']) 
def index():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    return render_template('annuaire.html', entries=contacts)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_contact():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        telephone = request.form['telephone']
        
        if len(telephone) != 10:
            return "Le numéro de téléphone doit comporter 10 chiffres. Veuillez réessayer."
        
        if not email.endswith('@gmail.com'):
            return "L'adresse e-mail doit se terminer par '@gmail.com'. Veuillez réessayer."

        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (nom, prenom, email, telephone) VALUES (?, ?, ?, ?)',
                       (nom, prenom, email, telephone))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('ajout.html')

@app.route('/modifier_contact/<int:contact_id>', methods=['GET', 'POST'])
def modifier_contact(contact_id):
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        telephone = request.form['telephone']
        
        if len(telephone) != 10:
            return "Le numéro de téléphone doit comporter 10 chiffres. Veuillez réessayer."
        
        if not email.endswith('@gmail.com'):
            return "L'adresse e-mail doit se terminer par '@gmail.com'. Veuillez réessayer."
        
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('UPDATE contacts SET nom =?, prenom =?, email =?, telephone =? WHERE id =?',
                       (nom, prenom, email, telephone, contact_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id =?', (contact_id,))
    modifie = cursor.fetchone()
    conn.close()
    return render_template('modifier_contact.html', modifie=[modifie])

@app.route('/supprimer/<int:contact_id>', methods=['GET', 'POST'])
def supprimer(contact_id):
    if request.method == 'GET':
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE id =?', (contact_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        pass

@app.route('/contact_details/<int:contact_id>', methods=['GET'])
def contact_details(contact_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id =?', (contact_id,))
    detail = cursor.fetchone()
    conn.close()
    return render_template('detail.html', detail=[detail])

@app.route('/rechercher', methods=['GET'])
def rechercher_contact():
    terme_recherche = request.args.get('search', '')  # Récupère le terme de recherche depuis l'URL
    
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE nom LIKE ? OR prenom LIKE ? OR email LIKE ? OR telephone LIKE ?",
                   ('%' + terme_recherche + '%', '%' + terme_recherche + '%', '%' + terme_recherche + '%', '%' + terme_recherche + '%'))
    contacts = cursor.fetchall()
    conn.close()

    return render_template('annuaire.html', entries=contacts)


if __name__ == '__main__':
    check_table_exists()
    app.run(debug=True)
