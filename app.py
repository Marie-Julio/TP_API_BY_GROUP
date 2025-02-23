from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
import pytesseract
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'secret_key'  # Clé secrète pour les sessions
bcrypt = Bcrypt(app)

# Configuration MySQL (XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'universite'

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

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# Route pour traiter le téléchargement de plusieurs fichiers
@app.route('/upload', methods=['POST'])
def upload_files():
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

    return render_template('result.html', extracted_text=all_extracted_text.strip())  # Supprimer les espaces inutiles

@app.route('/admin')
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

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/annees', methods=['GET'])

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
def enseignant():
    filter_prenom = request.args.get('filter_prenom')
    filter_specialite = request.args.get('filter_specialite')

    query = "SELECT id, nom, prenom, email, telephone, specialite FROM enseignant WHERE 1=1"
    filters = []
    if filter_prenom:
        query += " AND prenom LIKE %s"
        filters.append('%' + filter_prenom + '%')
    if filter_specialite:
        query += " AND specialite LIKE %s"
        filters.append('%' + filter_specialite + '%')

    data = fetch_data(query, filters) if filters else fetch_data(query)
    return render_template('enseignants.html', title='Enseignants', data=data, columns=['ID', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Spécialité'], table='enseignant', user=current_user)

@app.route('/filieres', methods=['GET'])
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

@app.route('/users', methods=['GET'])
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
    return render_template('users.html', title='Utilisateurs', data=data, columns=['ID', 'Nom', 'Prénom', 'Email', 'Rôle'], table='membre_administratif', user=current_user)

@app.route('/notes', methods=['GET'])
def note():
    filter_enseignant = request.args.get('filter_enseignant')
    filter_etudiant = request.args.get('filter_etudiant')
    filter_ue = request.args.get('filter_ue')

    query = """
        SELECT n.id, n.note, e.nom AS enseignant_nom, p.etudiant_matricule, u.nom AS ue_nom
        FROM note n
        JOIN parcours_etudiant p ON n.parcours_etudiant_id = p.id
        JOIN enseignant e ON e.id = n.ecue_id
        JOIN ue u ON u.id = n.ecue_id
        WHERE 1=1
    """
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

    data = fetch_data(query, filters) if filters else fetch_data(query)
    return render_template('notes.html', title='Notes', data=data, columns=['ID', 'Note', 'Enseignant', 'Matricule Étudiant', 'UE'], table='note', user=current_user)

@app.route('/parcours', methods=['GET'])
def parcours_etudiant():
    filter_matricule = request.args.get('filter_matricule')
    filter_annee = request.args.get('filter_annee')
    filter_annee_etude = request.args.get('filter_annee_etude')

    query = """
        SELECT p.id, p.etudiant_matricule, a.annee, ae.code, p.decision
        FROM parcours_etudiant p
        JOIN annee_academique a ON p.annee_academique_id = a.id
        JOIN annee_etude ae ON p.annee_etude_id = ae.id
        WHERE 1=1
    """
    filters = []

    if filter_matricule:
        query += " AND p.etudiant_matricule LIKE %s"
        filters.append('%' + filter_matricule + '%')
    if filter_annee:
        query += " AND a.annee LIKE %s"
        filters.append('%' + filter_annee + '%')
    if filter_annee_etude:
        query += " AND a.annee LIKE %s"
        filters.append('%' + filter_annee_etude + '%')

    data = fetch_data(query, filters) if filters else fetch_data(query)
    return render_template('parcours.html', title='Parcours Étudiant', data=data, columns=['ID', 'Matricule', 'Année Académique', 'Année Etude', 'Décision'], table='parcours_etudiant', user=current_user)

@app.route('/ues', methods=['GET'])
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



if __name__ == '__main__':
    app.run(debug=True)