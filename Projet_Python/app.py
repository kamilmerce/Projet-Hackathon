from flask import Flask, render_template, request, redirect, url_for # import de flask qui est un framework pour un rendu d'une page web
import sqlite3 # import sqlite3 pour l'accès à la base de données
import os # import os pour l'accès à la base de données avec un chemin

app = Flask(__name__) # création d'un objet Flask 

def connect_to_database(): # connexion à la base de données
    conn = sqlite3.connect('../Projet_Python/carnet_adresses.db')
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
    if not os.path.isfile('../Projet_Python/carnet_adresses.db'): # verifie si la base de données existe déjà
        conn = connect_to_database() # connexion à la base de données
        cursor = conn.cursor() # création d'un objet cursor qui permet de récupérer les donné
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
        
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts WHERE telephone=?', (telephone,))
        telephone_existe = cursor.fetchone()
        
        if telephone_existe:
            return "Le numéro de téléphone existe déjà. Veuillez réessayer."
        
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM contacts WHERE email=?', (email,))
        email_existe = cursor.fetchone()
        
        if email_existe:
            return "L'adresse e-mail existe déjà. Veuillez réessayer."
        
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
