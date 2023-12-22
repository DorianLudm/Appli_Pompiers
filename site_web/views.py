from .app import app, mkpath, db
from flask import render_template, url_for , redirect, request,  flash, session, send_from_directory
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user, logout_user, login_required, current_user
from .cache import documents
import webbrowser
import os
import random
from werkzeug.utils import secure_filename

active_tags = set()
tag_manuel = set()
filtre_texte = ""
selectType = "Choisir un type"

@app.route('/pompier')
@login_required
def home():
    """fonction d'affichage de la page d'accueil des pompiers"""
    global active_tags, documents
    result = []
    
    doc = None
    if request.args.get('id'):
        id = request.args['id']
        doc = get_document_id(id)
        doc.nomType = get_type(doc.idType).nomType
    
    if active_tags or filtre_texte:
        for i in get_types():
            resultat = dict()
            resultat["nomType"] = i.nomType
            resultat["element"] = []
            for document in get_document_types(i.idType, documents):
                resultat["element"].append(document)
            if resultat["element"]:
                result.append(resultat)
    info_doc = filtre_texte or "Rechercher un document !"
    return render_template("recherche_doc.html",tags = get_tags(), active_tags = active_tags, result = result, barre_recherche = info_doc, util = informations_utlisateurs(), title='Accueil',doc = doc)
 
@app.route('/ajouter_filtre/', methods =("POST",))
@login_required
def ajouter_filtre():
    """fonction d'ajout de filtre dans la recherche de documents"""
    global active_tags, filtre_texte, documents
    # Si aucun document n'est chargé
    if not documents:
        if not active_tags and not filtre_texte:
            documents = get_documents()
    # Si on recoit des infos par POST
    if request.method == 'POST':
        handle_filtrage()
    return redirect(url_for('home'))

@app.route('/ouverture_doc/<id>', methods =("POST",))
@login_required
def ouverture_doc(id):
    """fonction de redirection vers la page d'accueil"""
    return redirect(url_for('home', id=id))
  
@app.route('/visualiser/<id>', methods =("POST",))
@login_required
def visualiser(id):
    doc = get_document_id(id).fichierDoc
    webbrowser.open(mkpath('./static/document/' + doc)) 
    return redirect(url_for('home', id=id))

@app.route('/telecharger/<id>', methods =("POST",))
@login_required
def telecharger(id):
    path = mkpath('./static/document/')
    return send_from_directory(path, get_document_id(id).fichierDoc, as_attachment=True)
  


# LOGIN

class LoginForm( FlaskForm ):
    """formulaire de connexion"""
    identifiant = StringField('Identifiant')
    mdp = PasswordField('Password')
    def get_authentification_utilisateur(self):
        util = get_identifiant_utilisateur(self.identifiant.data)
        if util is None:
            return None
        m = sha256()
        m.update(self.mdp.data.encode())
        mdp = m.hexdigest()
        if mdp == util.mdp:
            return util
        else:
            return None

@app.route('/', methods=['GET', 'POST'])
def login():
    """fonction de connexion pour un utilisateur"""
    f = LoginForm()
    if f.validate_on_submit():
        util = f.get_authentification_utilisateur()
        if util:
            login_user(util)
            if current_user.idRole == -1: # Si l'utilisateur est un administrateur
                return redirect(url_for("home_admin"))
            else: # Alors l'utilisateur est un pompier
                return redirect(url_for("home"))
        else:
            return render_template(
                "login.html",
                form=f,
                erreur = "Login ou mot de passe incorrect")
    return render_template(
        "login.html",
        form=f,
        title='Page de connexion')

@app.route("/logout")
@login_required
def logout():
    """fonction de déconnexion"""
    logout_user()
    return redirect(url_for('login'))  

# ADMINISTRATION
@app.route('/administrateur')
def home_admin():
    """fonction de redirection vers l'accueil administrateur"""
    if not is_admin():
        return redirect(url_for('home'))
    return render_template('accueil_admin.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs(), title='Accueil administrateur')

@app.route('/administrateur/rechercheComptes')
@login_required
def recherche_comptes(searchNom="", selectGrade="Choisir un grade", selectCaserne="Choisir une caserne"):
    """redirection vers la page de recherche de compte"""
    if not is_admin():
        return redirect(url_for('home'))
    return render_template('rechercheComptes.html', title='Recherche de comptes', users=get_utilisateurs(), casernes = get_casernes(), grades = get_grades(), 
                            selectGrade=selectGrade, selectCaserne=selectCaserne, searchNom=searchNom, util = informations_utlisateurs())

@app.route('/administrateur/modifierCompte/<id>', methods=['GET', 'POST'])
@login_required
def modifier_compte(id):
    """redirection vers la page de modification d'un compte"""
    if not is_admin():
        return redirect(url_for('home'))
    user = Utilisateur.query.get(id)
    if request.form.get('save_compte') =="Sauvegarder le compte":
        user.nomUtilisateur = request.form.get('nom')
        user.prenomUtilisateur = request.form.get('prenom')
        user.identifiant = request.form.get('pseudo')
        if request.form.get('password') != "":
            user.mdp = sha256(request.form.get('password').encode()).hexdigest()
        user.idGrade = request.form.get('grades')
        user.idCas = request.form.get('casernes')
        db.session.commit() 
        return redirect(url_for('recherche_comptes')) 
    return render_template('modifierCompte.html', title='Modifier de Compte', user=user, grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs())

@app.route('/administrateur/rechercheDocAdmin')
@login_required
def recherche_doc_admin():
    """page de recherche des documents pour l'administrateur"""
    if not is_admin():
        return redirect(url_for('home'))
    global active_tags, selectType
    result = []
    # document = get_documents()
    for i in get_types():
        resultat = dict()
        resultat["nomType"] = i.nomType
        resultat["element"] = []
        
        for document in get_document_types(i.idType, documents):
            resultat["element"].append(document)
        result.append(resultat)
    return render_template("recherche_doc_admin.html",title="Admin | Recherche documents", tags = get_tags(), active_tags = active_tags, result = result, types= get_types(), util = informations_utlisateurs(), selectType=selectType, search=filtre_texte)

@app.route('/administrateur/modifierDocument/<id>', methods=['GET', 'POST'])
def modifier_document(id):
    """fonction de modification de document"""
    if not is_admin():
        return redirect(url_for('home'))
    doc = get_document_id(id)
    if request.form.get('modifier_document') =="Enregistrer":
        doc.nomDoc = request.form.get('titre')
        doc.idType = request.form.get('types')
        db.session.commit()
        global documents
        documents = []
        handle_filtrage(True)
        return redirect(url_for('recherche_doc_admin'))
    if request.form.get('annuler') =="Annuler":
        return redirect(url_for('recherche_doc_admin'))
    return render_template('modifier_document.html', title='Modifier le Document', doc=doc, types = get_types(), tags=get_tags(), util = informations_utlisateurs())

@app.route('/administrateur/ajouteDocument', methods=['GET', 'POST'])
@login_required
def ajoute_document():
    """fonction d'ajout d'un document"""
    if not is_admin():
        return redirect(url_for('home'))
    if request.method == 'POST':  
        if request.form.get('tag'):
            tag_a_supprimer = None
            for tag in tag_manuel:
                if tag.nomTag == request.form.get('tag'):
                    tag_a_supprimer = tag
            if tag_a_supprimer:
                tag_manuel.remove(tag_a_supprimer)            
        if request.form.get('tag-manuel'):
            est_present = False
            tag_ajoute = get_tag(request.form.get('tag-manuel'))
            for tag in tag_manuel:                
                if tag.nomTag == tag_ajoute.nomTag:
                    est_present = True
            if not est_present:
                tag = get_tag(request.form.get('tag-manuel'))
                if tag:
                    tag_manuel.add(tag)
        elif request.form.get('ajouter_document') =="Enregistrer":
            file = request.files['file']
            if request.form.get('type_document') != "Type":
                type = get_id_type(request.form.get('type_document'))
                document = Document(
                    nomDoc = request.form.get('titre'),
                    idType = type,
                    fichierDoc = request.form.get('repertoire')+"/"+secure_filename(file.filename),
                    descriptionDoc = request.form.get('description')
                )
                db.session.add(document)
                db.session.commit()
            if not os.path.exists(mkpath(os.path.join(app.config['UPLOAD_FOLDER'], request.form.get('repertoire')))):
                os.makedirs(mkpath(os.path.join(app.config['UPLOAD_FOLDER'], request.form.get('repertoire'))))
            file.save(mkpath(os.path.join(app.config['UPLOAD_FOLDER'], request.form.get('repertoire'), secure_filename(file.filename))))
            les_tags = request.form.get('repertoire').split("/")
            for tag in les_tags:
                if tag != "":
                    newtag = get_tag(tag, True)
                    for tag_actif in tag_manuel:
                        if tag_actif.nomTag == newtag.nomTag:
                            newtag = ""
                    if newtag:
                        document_tag = DocumentTag(
                            idDoc = document.idDoc,
                            idTag = newtag.idTag
                        )
                        db.session.add(document_tag)
                        db.session.commit()
                    if newtag is None:
                        a = hex(random.randrange(100,256))
                        b = hex(random.randrange(100,256))
                        c = hex(random.randrange(100,256))
                        tag = Tag(
                            idTag = get_max_id_tag()+1,
                            nomTag = tag,
                            couleurTag = a[2:]+b[2:]+c[2:]
                        )
                        db.session.add(tag)
                        db.session.commit()
                        document_tag = DocumentTag(
                            idDoc = document.idDoc,
                            idTag = tag.idTag
                        )
                        db.session.add(document_tag)
                        db.session.commit()
            tag_manuel.clear()
            return redirect(url_for('recherche_doc_admin')) 
        return render_template('ajouter_document.html', tags=get_tags(),document = request.files['file'], type =request.form.get('type_document'), util = informations_utlisateurs(),new_tag=tag_manuel,titre =request.form.get('titre'), description = request.form.get('description'), active_type = request.form.get('type_document'), repertoire = request.form.get('repertoire'),types = get_types(), title='Ajouter un document')
    return render_template('ajouter_document.html', types = get_types(), type = "Type",titre ="", description = "", tags=get_tags(),new_tag=tag_manuel, util = informations_utlisateurs(), title='Ajouter un document')

@app.route('/administrateur/appliquer_filtres', methods=['GET', 'POST'])
@login_required
def appliquer_filtres():
    """fonction de filtrage des comptes utilisateurs"""
    if not is_admin():
        return redirect(url_for('home'))
    if request.method == 'POST':
        if "reset" in request.form:
            return recherche_comptes()
        selectGrade = request.form.get('grades')
        selectCaserne = request.form.get('casernes')
        search_bar_value = request.form.get('search_bar')
        if selectGrade == "Tous les grades":
            selectGrade = "Choisir un grade"
        if selectCaserne == "Toutes les casernes":
            selectCaserne = "Choisir une caserne"
        return recherche_comptes(search_bar_value, selectGrade, selectCaserne)
    return recherche_comptes()

@app.route('/administrateur/appliquer_filtres_doc', methods=['GET', 'POST'])
@login_required
def ajouter_filtre_doc_admin():
    """fonction d'ajout de filtre pour la recherche de documents, partie administrateur"""
    if not is_admin():
        return redirect(url_for('home'))
    if request.method=='POST':
        handle_filtrage(True)
    return redirect(url_for('recherche_doc_admin'))

@app.route('/administrateur/supprimerDoc/<id>')
@login_required
def supprimer_document(id):
    """fonction de suppression d'un document"""
    if not is_admin():
        return redirect(url_for('home'))
    document = get_document_id(id)
    db.session.delete(document)
    db.session.commit()
    for doc in documents:
        if doc.idDoc == document.idDoc:
            documents.remove(doc)
    return redirect(url_for('recherche_doc_admin'))

class AjouteCompteForm(FlaskForm):
    """formulaire d'ajout de compte utilisateur"""
    nomUser = StringField('Nom', validators = [DataRequired()])
    prenomUser = StringField('Prenom', validators = [DataRequired()])
    pseudo = StringField("Nom d'utilisateur", validators = [DataRequired()])
    mdp = PasswordField('Mot de passe', validators = [DataRequired()])
    id_grade = SelectField('Grade', choices = [])
    id_caserne = SelectField('Caserne', choices = [])
    id_role = BooleanField('Administrateur ?')

@app.route('/administrateur/ajouteCompte')
@login_required
def ajoute_compte():
    """fonction d'ajoute de compte"""
    if not is_admin():
        return redirect(url_for('home'))
    f = AjouteCompteForm()
    f.id_grade.choices = [(g.idGrade, g.nomGrade) for g in get_grades()]
    f.id_caserne.choices = [(c.idCas, c.nomCaserne) for c in get_casernes()]
    return render_template('ajoute_compte.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs(), title='Ajouter un compte', form=f)

@app.route('/administrateur/supprimerCompte/<int:id>')
@login_required
def supprimer_compte(id):
    """fonction de suppression de compte"""
    if not is_admin():
        return redirect(url_for('home'))
    util = get_utilisateur(id)
    db.session.delete(util)
    db.session.commit()
    return redirect(url_for('recherche_comptes'))

@app.route("/administrateur/ajouteCompte/save", methods=["POST"])
def save_compte():
    """fonction d'enregistrement d'un nouveau compte"""
    if not is_admin():
        return redirect(url_for('home'))
    form = AjouteCompteForm()
    form.id_grade.choices = [(g.idGrade, g.nomGrade) for g in get_grades()]
    form.id_caserne.choices = [(c.idCas, c.nomCaserne) for c in get_casernes()]

    if form.validate_on_submit():
        if form.id_role.data:
            role = -1
        role = 1
        util = Utilisateur(
            idUtilisateur= max_id_utilisateur()+1,
            nomUtilisateur= form.nomUser.data,
            prenomUtilisateur= form.prenomUser.data,
            identifiant= form.pseudo.data,
            mdp= sha256(form.mdp.data.encode()).hexdigest(),
            idGrade= form.id_grade.data,
            idRole= role,
            idCas= form.id_caserne.data
        )
        db.session.add(util)
        db.session.commit()
        return redirect(url_for('recherche_comptes'))
    return render_template('ajoute_compte.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs(), title='Ajouter un compte', form=form)

def handle_filtrage(admin = False):
    global active_tags, filtre_texte, documents, selectType
    tag = request.form['tags']
    bool_fulldoc = False
    # Cas qui demande le chargement de tous les documents
    if not documents:
        if admin:
            if not active_tags and not filtre_texte and selectType == "Choisir un type":
                documents = get_documents()
                bool_fulldoc = True
        else:
            if not active_tags and not filtre_texte:
                documents = get_documents()
                bool_fulldoc = True
    if not bool_fulldoc and filtre_texte != request.form.get('barre_recherche'):
            documents = get_documents()
            bool_fulldoc = True
    if admin and not bool_fulldoc and selectType == "Choisir un type" and request.form.get('types') != "Choisir un type":
        selectType = request.form.get('types')
        documents = get_documents()
    # Filtre par type
    elif admin:
        selectType = "Choisir un type"
    # Recherche par mot ou ajout tag par point
    if request.form.get('barre_recherche'):
        if request.form.get('barre_recherche')[0] != ".":
            filtre_texte = request.form.get('barre_recherche')
            documents = get_filtrer_document_nom(documents, filtre_texte)
        else:
            tag = get_tag(request.form.get('barre_recherche')[1:])
            if tag:
                active_tags.add(tag)
                documents = get_filtrer_document_tag(documents, tag)
    else:
        filtre_texte = ""
    # Nouveau tag (existant en BD), alors on l'ajoute
    if tag != "Choisir un tag":
        tag = get_tag(request.form.get('tags'), True)
        if tag:
            already_in = False
            for t in active_tags:
                if t.nomTag == tag.nomTag:
                    already_in = True
            if not already_in:
                active_tags.add(tag)
                documents = get_filtrer_document_tag(documents, tag)
    # Suppression d'un tag lorsqu'on appuie sur celui-ci
    if request.form.get('retirer_filtre'):
        tag_to_delete = []
        for tag in active_tags:
            if tag.nomTag == request.form.get('retirer_filtre'):
                tag_to_delete.append(tag)
        for tag in tag_to_delete:
            active_tags.remove(tag)
                
        documents = get_documents()
        if filtre_texte:
            documents = get_filtrer_document_nom(documents, filtre_texte)
        for tag in active_tags:
            documents = get_filtrer_document_tag(documents, tag)
    
    if request.form.get('reset'):
        if admin:
            selectType = "Choisir un type"
            active_tags = set()
            filtre_texte = ""
            documents = []
            return redirect(url_for('recherche_doc_admin'))
        active_tags = set()
        filtre_texte = ""
        documents = []
        return redirect(url_for('home'))
    
    # Si il y a aucun critère de recherche, alors on load aucun document
    if admin:
        if not active_tags and not filtre_texte and selectType == "Choisir un type":
            documents = []
    else:
        if not active_tags and not filtre_texte:
            documents = []

@app.route("/administrateur/gerer_compte/erreur")
@login_required
def erreur_compte():
    """fonction destinée à gérer les erreurs de connexion"""
    if not is_admin():
        return redirect(url_for('home'))
    print("\nerreur\n")
