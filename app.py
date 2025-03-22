from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from PIL import Image
import pytesseract
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flasgger import Swagger

app = Flask(__name__)
app.secret_key = 'secret_key'  # Clé secrète pour les sessions
bcrypt = Bcrypt(app)

# Configuration MySQL (XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'entite'

# Configuration de Swagger
app.config['SWAGGER'] = {
    'title': 'API Documentation',
    'uiversion': 3,
    'description': 'Documentation for the API endpoints',
    'version': '1.0.0',
}

swagger = Swagger(app)

# ----------------------------------------------------------------------------------------

# Connexion MySQL
mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

# Gestion des sessions avec Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role

def fetch_data(query, params=None):
    cursor = mysql.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

# Chemin pour enregistrer les fichiers téléchargés
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}

# Fonction pour vérifier si le fichier est valide
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.cursor(dictionary=True)
    cursor.execute("SELECT * FROM membre_administratif WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user['id'], user['email'], user['role'])
    return None

@app.route('/api/annee_academique', methods=['GET', 'POST'])
def manage_annee_academique():
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO annee_academique (annee) VALUES (%s)", (data['annee'],))
        conn.commit()
        return jsonify({'message': 'Année académique ajoutée'}), 201
    
    cursor.execute("SELECT * FROM annee_academique")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/annee_academique/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_annee_academique(id):
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM annee_academique WHERE id = %s", (id,))
        result = cursor.fetchone()
        return jsonify(result) if result else ('', 404)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE annee_academique SET annee = %s WHERE id = %s", (data['annee'], id))
        conn.commit()
        return jsonify({'message': 'Mise à jour effectuée'})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM annee_academique WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Suppression effectuée'})

@app.route('/api/grade', methods=['GET', 'POST'])
def manage_grade():
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO grade (nom) VALUES (%s)", (data['nom'],))
        conn.commit()
        return jsonify({'message': 'Grade ajouté'}), 201
    
    cursor.execute("SELECT * FROM grade")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/grade/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_grade(id):
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM grade WHERE id = %s", (id,))
        result = cursor.fetchone()
        return jsonify(result) if result else ('', 404)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE grade SET nom = %s WHERE id = %s", (data['nom'], id))
        conn.commit()
        return jsonify({'message': 'Mise à jour effectuée'})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM grade WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Suppression effectuée'})

# Ajout des routes pour les autres tables
# Exemple pour la table etudiant
@app.route('/api/etudiant', methods=['GET', 'POST'])
def manage_etudiant():
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO etudiant (matricule, nom, prenom, date_naissance, sexe, email, telephone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (data['matricule'], data['nom'], data['prenom'], data['date_naissance'], data['sexe'], data['email'], data.get('telephone')))
        conn.commit()
        return jsonify({'message': 'Étudiant ajouté'}), 201
    
    cursor.execute("SELECT * FROM etudiant")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/etudiant/<string:matricule>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_etudiant(matricule):
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM etudiant WHERE matricule = %s", (matricule,))
        result = cursor.fetchone()
        return jsonify(result) if result else ('', 404)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE etudiant SET nom = %s, prenom = %s, date_naissance = %s, sexe = %s, email = %s, telephone = %s WHERE matricule = %s",
                    (data['nom'], data['prenom'], data['date_naissance'], data['sexe'], data['email'], data.get('telephone'), matricule))
        conn.commit()
        return jsonify({'message': 'Mise à jour effectuée'})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM etudiant WHERE matricule = %s", (matricule,))
        conn.commit()
        return jsonify({'message': 'Suppression effectuée'})


@app.route('/api/annee_etude', methods=['GET', 'POST'])
def manage_annee_etude():
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO annee_etude (code, niveau, filiere_id, grade_id) VALUES (%s, %s, %s, %s)",
                       (data['code'], data['niveau'], data.get('filiere_id'), data.get('grade_id')))
        conn.commit()
        return jsonify({'message': 'Année d’étude ajoutée'}), 201
    
    cursor.execute("SELECT * FROM annee_etude")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/annee_etude/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_annee_etude(id):
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM annee_etude WHERE id = %s", (id,))
        result = cursor.fetchone()
        return jsonify(result) if result else ('', 404)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE annee_etude SET code = %s, niveau = %s, filiere_id = %s, grade_id = %s WHERE id = %s",
                       (data['code'], data['niveau'], data.get('filiere_id'), data.get('grade_id'), id))
        conn.commit()
        return jsonify({'message': 'Mise à jour effectuée'})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM annee_etude WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Suppression effectuée'})

@app.route('/api/ecue', methods=['GET', 'POST'])
def manage_ecue():
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO ecue (code, nom, ue_id, enseignant_id) VALUES (%s, %s, %s, %s)",
                       (data['code'], data['nom'], data.get('ue_id'), data.get('enseignant_id')))
        conn.commit()
        return jsonify({'message': 'ECUE ajoutée'}), 201
    
    cursor.execute("SELECT * FROM ecue")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/ecue/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_ecue(id):
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM ecue WHERE id = %s", (id,))
        result = cursor.fetchone()
        return jsonify(result) if result else ('', 404)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE ecue SET code = %s, nom = %s, ue_id = %s, enseignant_id = %s WHERE id = %s",
                       (data['code'], data['nom'], data.get('ue_id'), data.get('enseignant_id'), id))
        conn.commit()
        return jsonify({'message': 'Mise à jour effectuée'})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM ecue WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Suppression effectuée'})

@app.route('/api/enseignant', methods=['GET', 'POST'])
def manage_enseignant():
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO enseignant (nom, prenom, email, telephone, specialite) VALUES (%s, %s, %s, %s, %s)",
                       (data['nom'], data['prenom'], data['email'], data.get('telephone'), data['specialite']))
        conn.commit()
        return jsonify({'message': 'Enseignant ajouté'}), 201
    
    cursor.execute("SELECT * FROM enseignant")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/enseignant/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_enseignant(id):
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM enseignant WHERE id = %s", (id,))
        result = cursor.fetchone()
        return jsonify(result) if result else ('', 404)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE enseignant SET nom = %s, prenom = %s, email = %s, telephone = %s, specialite = %s WHERE id = %s",
                       (data['nom'], data['prenom'], data['email'], data.get('telephone'), data['specialite'], id))
        conn.commit()
        return jsonify({'message': 'Mise à jour effectuée'})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM enseignant WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Suppression effectuée'})
    
@app.route('/api/ue', methods=['GET', 'POST'])
def manage_ue():
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO ue (code, nom, annee_etude_id) VALUES (%s, %s, %s)", 
                       (data['code'], data['nom'], data.get('annee_etude_id')))
        conn.commit()
        return jsonify({'message': 'UE ajoutée'}), 201
    
    cursor.execute("SELECT * FROM ue")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/ue/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_ue(id):
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM ue WHERE id = %s", (id,))
        result = cursor.fetchone()
        return jsonify(result) if result else ('', 404)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE ue SET code = %s, nom = %s, annee_etude_id = %s WHERE id = %s",
                       (data['code'], data['nom'], data.get('annee_etude_id'), id))
        conn.commit()
        return jsonify({'message': 'Mise à jour effectuée'})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM ue WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Suppression effectuée'})

@app.route('/api/note', methods=['GET', 'POST'])
def manage_note():
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO note (ecue_id, parcours_etudiant_id, note) VALUES (%s, %s, %s)",
                       (data['ecue_id'], data['parcours_etudiant_id'], data['note']))
        conn.commit()
        return jsonify({'message': 'Note ajoutée'}), 201
    
    cursor.execute("SELECT * FROM note")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/note/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_note(id):
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM note WHERE id = %s", (id,))
        result = cursor.fetchone()
        return jsonify(result) if result else ('', 404)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE note SET ecue_id = %s, parcours_etudiant_id = %s, note = %s WHERE id = %s",
                       (data['ecue_id'], data['parcours_etudiant_id'], data['note'], id))
        conn.commit()
        return jsonify({'message': 'Mise à jour effectuée'})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM note WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Suppression effectuée'})

@app.route('/api/parcours_etudiant', methods=['GET', 'POST'])
def manage_parcours_etudiant():
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO parcours_etudiant (etudiant_matricule, annee_etude_id, annee_academique_id, decision) VALUES (%s, %s, %s, %s)",
                       (data['etudiant_matricule'], data['annee_etude_id'], data['annee_academique_id'], data['decision']))
        conn.commit()
        return jsonify({'message': 'Parcours étudiant ajouté'}), 201
    
    cursor.execute("SELECT * FROM parcours_etudiant")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/parcours_etudiant/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_parcours_etudiant(id):
    conn = mysql
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM parcours_etudiant WHERE id = %s", (id,))
        result = cursor.fetchone()
        return jsonify(result) if result else ('', 404)
    
    if request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE parcours_etudiant SET etudiant_matricule = %s, annee_etude_id = %s, annee_academique_id = %s, decision = %s WHERE id = %s",
                       (data['etudiant_matricule'], data['annee_etude_id'], data['annee_academique_id'], data['decision'], id))
        conn.commit()
        return jsonify({'message': 'Mise à jour effectuée'})
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM parcours_etudiant WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'Suppression effectuée'})

# ----------------------------------------------------------------------------------------

# Route principale
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM membre_administratif WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user['mot_de_passe'], password):
            login_user(User(user['id'], user['email'], user['role']))
            return redirect(url_for('dashboard'))
        else:
            flash("Identifiants incorrects", "danger")
    return render_template('index.html')

@app.route('/addupload')
@login_required
def addupload():
    return render_template('addupload.html')

# Route pour traiter le téléchargement de plusieurs fichiers
@app.route('/upload', methods=['POST'])
@login_required
def upload_files():
    annee = request.form.get('annee')
    annee_etude = request.form.get('annee_etude')
    ecue = request.form.get('ecue')
    ue = request.form.get('ue')

    if 'file' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('file')  # Récupérer plusieurs fichiers
    all_extracted_text = ""  # Stocker tout le texte extrait

    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Sauvegarder chaque fichier téléchargé
            file.save(file_path)
            
            # Extraire le texte de l'image avec Tesseract
            image = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(image)

            # Concaténer les résultats
            all_extracted_text += extracted_text + "\n\n"

    return render_template('result.html', title='Notes', annee=annee, ecue=ecue, ue=ue, annee_etude=annee_etude, extracted_text=all_extracted_text.strip(), user=current_user)

@app.route('/admin')
@login_required
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM membre_administratif WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user['mot_de_passe'], password):
            login_user(User(user['id'], user['email'], user['role']))
            return redirect(url_for('dashboard'))
        else:
            flash("Identifiants incorrects", "danger")

    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Vérifier si l'utilisateur existe déjà
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM membre_administratif WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Un compte avec cet email existe déjà.", "danger")
            return redirect(url_for('create_account'))

        # Hachage du mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insérer le nouvel utilisateur dans la base de données
        cursor.execute("INSERT INTO membre_administratif (nom, prenom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s, %s)", (nom, prenom, email, hashed_password, role))
        mysql.commit()
        cursor.close()

        flash("Compte créé avec succès ! Vous pouvez vous connecter.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/annees', methods=['GET'])
@login_required
def annee_academique():
    filter_annee = request.args.get('filter_annee')
    
    query = "SELECT id, annee FROM annee_academique WHERE 1=1"
    filters = []
    if filter_annee:
        query += " AND annee LIKE %s"
        filters.append('%' + filter_annee + '%')

    data = fetch_data(query, filters) if filters else fetch_data(query)

    filter2_nom = request.args.get('filter_nom')

    query2 = "SELECT id, nom FROM grade WHERE 1=1"
    filters2 = []
    if filter2_nom:
        query += " AND nom LIKE %s"
        filters2.append('%' + filter2_nom + '%')

    data2 = fetch_data(query2, filters2) if filters2 else fetch_data(query2)
    return render_template('annees.html', title='Années & Grades', data=data, data2=data2, columns=['ID', 'Année'], columns2=['ID', 'Nom'], table='annee_academique', user=current_user)

@app.route('/enseignants', methods=['GET'])
@login_required
def enseignant():
    filter_nom = request.args.get('filter_nom')
    filter_prenom = request.args.get('filter_prenom')
    filter_email = request.args.get('filter_email')
    filter_specialite = request.args.get('filter_specialite')

    query = "SELECT id, nom, prenom, email, specialite FROM enseignant WHERE 1=1"
    filters = []
    if filter_nom:
        query += " AND nom LIKE %s"
        filters.append('%' + filter_nom + '%')
    if filter_prenom:
        query += " AND prenom LIKE %s"
        filters.append('%' + filter_prenom + '%')
    if filter_email:
        query += " AND email LIKE %s"
        filters.append('%' + filter_email + '%')
    if filter_specialite:
        query += " AND specialite LIKE %s"
        filters.append('%' + filter_specialite + '%')

    data = fetch_data(query, filters) if filters else fetch_data(query)
    return render_template('enseignants.html', title='Enseignants', data=data, columns=['ID', 'Nom', 'Prénom', 'Email', 'Spécialité'], table='enseignant', user=current_user)

@app.route('/filieres', methods=['GET'])
@login_required
def filiere():
    filter_code = request.args.get('filter_code')
    filter_nom = request.args.get('filter_nom')
    filter_mention = request.args.get('filter_mention')
    filter_domaine = request.args.get('filter_domaine')

    query = "SELECT id, code, nom, mention, domaine FROM filiere WHERE 1=1"
    filters = []
    if filter_code:
        query += " AND code LIKE %s"
        filters.append('%' + filter_code + '%')
    if filter_nom:
        query += " AND nom LIKE %s"
        filters.append('%' + filter_nom + '%')
    if filter_mention:
        query += " AND nom LIKE %s"
        filters.append('%' + filter_mention + '%')
    if filter_domaine:
        query += " AND nom LIKE %s"
        filters.append('%' + filter_domaine + '%')

    data = fetch_data(query, filters) if filters else fetch_data(query)
    return render_template('filieres.html', title='Filières', data=data, columns=['ID', 'Code', 'Nom', 'Mention', 'Domaine'], table='filiere', user=current_user)

@app.route('/users', methods=['GET', 'POST'])
@login_required
def membre_administratif():
    filter_nom = request.args.get('filter_nom')
    filter_prenom = request.args.get('filter_prenom')
    filter_email = request.args.get('filter_email')

    query = "SELECT id, nom, prenom, email, role FROM membre_administratif WHERE 1=1"
    filters = []
    if filter_nom:
        query += " AND nom LIKE %s"
        filters.append('%' + filter_nom + '%')
    if filter_prenom:
        query += " AND prenom LIKE %s"
        filters.append('%' + filter_prenom + '%')
    if filter_email:
        query += " AND email LIKE %s"
        filters.append('%' + filter_email + '%')

    data = fetch_data(query, filters) if filters else fetch_data(query)

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Vérifier si l'utilisateur existe déjà
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM membre_administratif WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Un compte avec cet email existe déjà.", "danger")
            return redirect(url_for('create_account'))

        # Hachage du mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insérer le nouvel utilisateur dans la base de données
        cursor.execute("INSERT INTO membre_administratif (nom, prenom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s, %s)", (nom, prenom, email, hashed_password, role))
        mysql.commit()
        cursor.close()

        flash("Compte créé avec succès ! Vous pouvez vous connecter.", "success")
        
    return render_template('users.html', title='Utilisateurs', data=data, columns=['ID', 'Nom', 'Prénom', 'Email', 'Rôle'], table='membre_administratif', user=current_user)

@app.route('/notes', methods=['GET'])
@login_required
def note():
    filter_enseignant = request.args.get('filter_enseignant')
    filter_etudiant = request.args.get('filter_etudiant')
    filter_ue = request.args.get('filter_ue')

    query = """
        SELECT n.id, p.etudiant_matricule, n.note, u.nom AS ue_nom
        FROM note n
        JOIN parcours_etudiant p ON n.parcours_etudiant_id = p.id
        JOIN ecue u ON u.id = n.ecue_id
        WHERE 1=1
    """
    queryf = "SELECT id, code, nom, mention, domaine FROM filiere WHERE 1=1"
    querya = "SELECT id, annee FROM annee_academique WHERE 1=1"
    queryg = "SELECT id, nom FROM grade WHERE 1=1"
    queryue = "SELECT id, code, nom FROM ue WHERE 1=1"
    queryec = "SELECT id, code, nom FROM ecue WHERE 1=1"
    querye = "SELECT id, code FROM annee_etude WHERE 1=1"
    filters = []
    if filter_enseignant:
        query += " AND e.nom LIKE %s"
        filters.append('%' + filter_enseignant + '%')
    if filter_etudiant:
        query += " AND p.etudiant_matricule LIKE %s"
        filters.append('%' + filter_etudiant + '%')
    if filter_ue:
        query += " AND u.nom LIKE %s"
        filters.append('%' + filter_ue + '%')
    query += " ORDER BY id DESC"

    data = fetch_data(query, filters) if filters else fetch_data(query)
    dataa = fetch_data(querya,)
    dataf = fetch_data(queryf,)
    datag = fetch_data(queryg,)
    dataue = fetch_data(queryue,)
    dataec = fetch_data(queryec,)
    datae = fetch_data(querye,)
    return render_template('notes.html', title='Notes', data=data, dataa=dataa, datag=datag, dataf=dataf, datae=datae, dataue=dataue, dataec=dataec, columns=['ID', 'Matricule Étudiant', 'Note', 'ECUE'], table='note', user=current_user)

@app.route('/parcours', methods=['GET'])
@login_required
def parcours_etudiant():
    filter_matricule = request.args.get('filter_matricule')
    filter_annee = request.args.get('filter_annee')
    filter_filiere = request.args.get('filter_filiere')
    filter_grade = request.args.get('filter_grade')
    filter_niveau = request.args.get('filter_niveau')

    query = """
        SELECT p.id, p.etudiant_matricule, a.annee, ae.code, p.semestre, p.decision
        FROM parcours_etudiant p
        JOIN annee_academique a ON p.annee_academique_id = a.id
        JOIN annee_etude ae ON p.annee_etude_id = ae.id
        WHERE 1=1
    """
    queryf = "SELECT id, code, nom, mention, domaine FROM filiere WHERE 1=1"
    querya = "SELECT id, annee FROM annee_academique WHERE 1=1"
    queryg = "SELECT id, nom FROM grade WHERE 1=1"
    filters = []

    if filter_matricule:
        query += " AND p.etudiant_matricule LIKE %s"
        filters.append('%' + filter_matricule + '%')
    if filter_annee:
        query += " AND p.annee_academique_id LIKE %s"
        filters.append('%' + filter_annee + '%')
    if filter_filiere:
        query += " AND ae.filiere_id LIKE %s"
        filters.append('%' + filter_filiere + '%')
    if filter_grade:
        query += " AND ae.grade_id LIKE %s"
        filters.append('%' + filter_grade + '%')
    if filter_niveau:
        query += " AND ae.niveau LIKE %s"
        filters.append('%' + filter_niveau + '%')

    data = fetch_data(query, filters) if filters else fetch_data(query)
    dataa = fetch_data(querya,)
    dataf = fetch_data(queryf,)
    datag = fetch_data(queryg,)
    return render_template('parcours.html', title='Parcours Étudiant', data=data, dataa=dataa, datag=datag, dataf=dataf, columns=['ID', 'Matricule', 'Année Académique', 'Année Etude', 'Semestre', 'Décision'], table='parcours_etudiant', user=current_user)

@app.route('/offres', methods=['GET'])
@login_required
def offres():
    filter_annee = request.args.get('filter_annee')
    filter_filiere = request.args.get('filter_filiere')
    filter_grade = request.args.get('filter_grade')
    filter_niveau = request.args.get('filter_niveau')

    query = """
        SELECT u.semestre, u.code, u.nom, u.credit, e.code, e.nom
        FROM ecue e
        JOIN ue u ON e.ue_id = u.id
        JOIN annee_etude ae ON u.annee_etude_id = ae.id
        WHERE 1=1 
    """
    queryf = "SELECT id, code, nom, mention, domaine FROM filiere WHERE 1=1"
    querya = "SELECT id, annee FROM annee_academique WHERE 1=1"
    queryg = "SELECT id, nom FROM grade WHERE 1=1"
    filters = []

    if filter_annee:
        query += " AND p.annee_academique_id LIKE %s"
        filters.append('%' + filter_annee + '%')
    if filter_filiere:
        query += " AND ae.filiere_id LIKE %s"
        filters.append('%' + filter_filiere + '%')
    if filter_grade:
        query += " AND ae.grade_id LIKE %s"
        filters.append('%' + filter_grade + '%')
    if filter_niveau:
        query += " AND ae.niveau LIKE %s"
        filters.append('%' + filter_niveau + '%')

    data = fetch_data(query, filters) if filters else fetch_data(query)
    dataa = fetch_data(querya,)
    dataf = fetch_data(queryf,)
    datag = fetch_data(queryg,)
    return render_template('offres.html', title='Offres de Formation', data=data, dataa=dataa, datag=datag, dataf=dataf, columns=['Semestre', 'Code UE', 'Institulé UE', 'Credit', 'code ECUE', 'Institulé ECUE'], table='offres', user=current_user)


@app.route('/ues', methods=['GET'])
@login_required
def ue():
    filter_id = request.args.get('filter_id')
    filter_code = request.args.get('filter_code')
    filter_nom = request.args.get('filter_nom')
    filter_annee = request.args.get('filter_annee')

    query = """
        SELECT u.id, u.code, u.nom, a.annee
        FROM ue u
        JOIN annee_academique a ON u.annee_etude_id = a.id
        WHERE 1=1
    """
    filters = []

    if filter_id:
        query += " AND u.id = %s"
        filters.append(filter_id)
    if filter_code:
        query += " AND u.code LIKE %s"
        filters.append('%' + filter_code + '%')
    if filter_nom:
        query += " AND u.nom LIKE %s"
        filters.append('%' + filter_nom + '%')
    if filter_annee:
        query += " AND a.annee LIKE %s"
        filters.append('%' + filter_annee + '%')

    data = fetch_data(query, filters) if filters else fetch_data(query)
    return render_template('ues.html', title='Unités d’Enseignement', data=data, columns=['ID', 'Code', 'Nom', 'Année'], table='ue', user=current_user)

@app.route('/etudiants', methods=['GET'])
@login_required
def etudiant():
    filter_matricule = request.args.get('filter_matricule')
    filter_nom = request.args.get('filter_nom')
    filter_prenom = request.args.get('filter_prenom')
    filter_annee = request.args.get('filter_annee')

    query = """
        SELECT matricule, nom, prenom, date_naissance, telephone
        FROM etudiant
        WHERE 1=1
    """
    filters = []

    if filter_matricule:
        query += " AND matricule LIKE %s"
        filters.append('%' + filter_matricule + '%')
    if filter_nom:
        query += " AND nom LIKE %s"
        filters.append('%' + filter_nom + '%')
    if filter_prenom:
        query += " AND prenom LIKE %s"
        filters.append('%' + filter_prenom + '%')
    if filter_annee:
        query += " AND annee_etude_id = %s"  # Ajustez cette condition selon votre structure de données
        filters.append(filter_annee)

    data = fetch_data(query, filters) if filters else fetch_data(query)
    return render_template('etudiants.html', title='Étudiants', data=data, columns=['Matricule', 'Nom', 'Prénom', 'Date de Naissance', 'Téléphone'], table='etudiant', user=current_user)

# Add routes for creating new records

@app.route('/add/annee', methods=['POST'])
@login_required
def add_annee():
    annee = request.form.get('annee')
    query = "INSERT INTO annee_academique (annee) VALUES (%s)"
    execute_query(query, (annee,))
    return redirect(url_for('annee_academique'))

@app.route('/add/user', methods=['POST'])
@login_required
def add_user():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Vérifier si l'utilisateur existe déjà
        cursor = mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM membre_administratif WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Un compte avec cet email existe déjà.", "danger")
            return redirect(url_for('create_account'))

        # Hachage du mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insérer le nouvel utilisateur dans la base de données
        cursor.execute("INSERT INTO membre_administratif (nom, prenom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s, %s)", (nom, prenom, email, hashed_password, role))
        mysql.commit()
        cursor.close()

    return redirect(url_for('users'))

@app.route('/add/grade', methods=['POST'])
@login_required
def add_grade():
    nom = request.form.get('nom')
    query = "INSERT INTO grade (nom) VALUES (%s)"
    execute_query(query, (nom,))
    return redirect(url_for('annee_academique'))

@app.route('/add/enseignant', methods=['POST'])
@login_required
def add_enseignant():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    specialite = request.form.get('specialite')
    
    query = "INSERT INTO enseignant (nom, prenom, email, telephone, specialite) VALUES (%s, %s, %s, %s, %s)"
    execute_query(query, (nom, prenom, email, telephone, specialite))
    return redirect(url_for('enseignant'))

@app.route('/add/filiere', methods=['POST'])
@login_required
def add_filiere():
    code = request.form.get('code')
    nom = request.form.get('nom')
    mention = request.form.get('mention')
    domaine = request.form.get('domaine')
    
    query = "INSERT INTO filiere (code, nom, mention, domaine) VALUES (%s, %s, %s, %s)"
    execute_query(query, (code, nom, mention, domaine))
    return redirect(url_for('filiere'))

@app.route('/add/note', methods=['POST'])
@login_required
def add_note():
    data = request.json
    ecue = data.get('ecue')
    annee_etude = data.get('annee_etude')
    annee = data.get('annee')
    ue = data.get('ue')
    notes = data.get('notes')

    if not notes:
        return jsonify({'error': 'Aucune note fournie'}), 400
    for entry in notes:
        matricule = entry.get('matricule')
        note = entry.get('note')

        if matricule and note:
            
            query0 = """
                SELECT semestre FROM ue 
                WHERE 1=1
            """
            filters = []
            if ue:
                query0 += " AND id = %s"  # Ajustez cette condition selon votre structure de données
                filters.append(ue)
                data0 = fetch_data(query0, filters)
                if matricule and annee_etude and annee and data0[0][0] :
                    query = """
                        SELECT id FROM parcours_etudiant 
                        WHERE etudiant_matricule = %s AND annee_etude_id = %s AND annee_academique_id = %s AND semestre = %s
                    """
                    data = fetch_data(query, (matricule, annee_etude, annee, data0[0][0]))
                    if data:
                        parcours_etudiant_id = data[0][0]

                        query = "INSERT INTO note (note, parcours_etudiant_id, ecue_id) VALUES (%s, %s, %s)"
                        execute_query(query, (note, parcours_etudiant_id, ecue))
    
    return jsonify({'success': True})

@app.route('/add/parcours_etudiant', methods=['POST'])
@login_required
def add_parcours_etudiant():
    etudiant_matricule = request.form.get('etudiant_matricule')
    annee_academique_id = request.form.get('annee_academique_id')
    annee_etude_id = request.form.get('annee_etude_id')
    decision = request.form.get('decision')
    
    query = "INSERT INTO parcours_etudiant (etudiant_matricule, annee_academique_id, annee_etude_id, decision) VALUES (%s, %s, %s, %s)"
    execute_query(query, (etudiant_matricule, annee_academique_id, annee_etude_id, decision))
    return redirect(url_for('parcours_etudiant'))

@app.route('/add/ue', methods=['POST'])
@login_required
def add_ue():
    code = request.form.get('code')
    nom = request.form.get('nom')
    annee_etude_id = request.form.get('annee_etude_id')
    
    query = "INSERT INTO ue (code, nom, annee_etude_id) VALUES (%s, %s, %s)"
    execute_query(query, (code, nom, annee_etude_id))
    return redirect(url_for('ue'))

@app.route('/add/etudiant', methods=['POST'])
@login_required
def add_etudiant():
    matricule = request.form.get('matricule')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date_naissance = request.form.get('date_naissance')
    telephone = request.form.get('telephone')
    
    query = "INSERT INTO etudiant (matricule, nom, prenom, date_naissance, telephone) VALUES (%s, %s, %s, %s, %s)"
    execute_query(query, (matricule, nom, prenom, date_naissance, telephone))
    return redirect(url_for('etudiant'))

def execute_query(query, params=None):
    conn = mysql
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        flash("Opération réussie", "success")
    except Exception as e:
        print(f"Error executing query: {e}")
        flash(f"Error: {str(e)}", "error")
    finally:
        cursor.close()


@app.route('/delete/annee/<int:id>', methods=['GET'])
@login_required
def delete_annee(id):
    query = "DELETE FROM annee_academique WHERE id = %s"
    execute_query(query, (id,))
    return redirect(url_for('annee_academique'))

@app.route('/delete/grade/<int:id>', methods=['GET'])
@login_required
def delete_grade(id):
    query = "DELETE FROM grade WHERE id = %s"
    execute_query(query, (id,))   
    return redirect(url_for('annee_academique'))

@app.route('/delete/enseignant/<int:id>', methods=['GET'])
@login_required
def delete_enseignant(id):
    query = "DELETE FROM enseignant WHERE id = %s"
    execute_query(query, (id,))
    return redirect(url_for('enseignant'))

@app.route('/delete/filiere/<int:id>', methods=['GET'])
@login_required
def delete_filiere(id):
    query = "DELETE FROM filiere WHERE id = %s"
    execute_query(query, (id,))
    return redirect(url_for('filiere'))

@app.route('/delete/membre_administratif/<int:id>', methods=['GET'])
@login_required
def delete_membre_administratif(id):
    query = "DELETE FROM membre_administratif WHERE id = %s"
    execute_query(query, (id,))
    return redirect(url_for('membre_administratif'))

@app.route('/delete/note/<int:id>', methods=['GET'])
@login_required
def delete_note(id):
    query = "DELETE FROM note WHERE id = %s"
    execute_query(query, (id,))
    return redirect(url_for('note'))

@app.route('/delete/parcours_etudiant/<int:id>', methods=['GET'])
@login_required
def delete_parcours_etudiant(id):
    query = "DELETE FROM parcours_etudiant WHERE id = %s"
    execute_query(query, (id,))
    return redirect(url_for('parcours_etudiant'))

@app.route('/delete/ue/<int:id>', methods=['GET'])
@login_required
def delete_ue(id):
    query = "DELETE FROM ue WHERE id = %s"
    execute_query(query, (id,))
    return redirect(url_for('ue'))

@app.route('/delete/etudiant/<matricule>', methods=['GET'])
@login_required
def delete_etudiant(matricule):
    query = "DELETE FROM etudiant WHERE matricule = %s LIMIT 1"
    execute_query(query, (matricule,))
    return redirect(url_for('etudiant'))

if __name__ == '__main__':
    app.run(debug=True)