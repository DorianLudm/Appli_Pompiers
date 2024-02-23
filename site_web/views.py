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
import shutil
from .generationTag import generationTag, generationTagDossier

active_tags = set()
tag_manuel = set()
filtre_texte = ""
selectType = "Choisir un type"
favoris = False
extension = ""

@app.route('/pompier')
@login_required
def home():
    """fonction d'affichage de la page d'accueil des pompiers"""
    global active_tags, documents, favoris, extension
    result = []
    extensions = ["pdf", "doc", "docx", "odf", "txt", "jpg", "jpeg", "png", "gif"]
    doc = None
    is_stared = False
    if request.args.get('id'):
        id = request.args['id']
        doc = get_document_id(id)
        doc.nomType = get_type(doc.idType).nomType
        is_stared = user_has_favoris(current_user.idUtilisateur, id)

    if active_tags or filtre_texte or favoris:
        for i in get_types():
            resultat = dict()
            resultat["nomType"] = i.nomType
            resultat["element"] = []
            for document in get_document_types(i.idType, documents):
                resultat["element"].append(document)
            if resultat["element"]:
                result.append(resultat)
    info_doc = filtre_texte or "Rechercher un document !"
    extension = extension or "Choisir une extension"
    return render_template("recherche_doc.html",tags = get_tags(), extensions = extensions, extension_actuelle = extension, active_tags = active_tags, result = result, barre_recherche = info_doc, util = informations_utlisateurs(), title='Accueil',doc = doc, favoris_on = favoris, is_stared = is_stared)

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

@app.route("/ajouter_favoris/<id>", methods =("POST",))
@login_required
def ajouter_favoris(id):
    if user_has_favoris(current_user.idUtilisateur, id):
        remove_favoris(current_user.idUtilisateur, id)
        handle_filtrage(False, True)
    else:
        add_favoris(current_user.idUtilisateur, id)
    return redirect(url_for('home', id=id))

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

class MdpOublieForm( FlaskForm ):
    """formulaire de mot de passe oublié"""
    identifiant = StringField('Identifiant')
    mdp = PasswordField('Password')
    mdpConfirm = PasswordField('Confirm Password')
    def get_authentification_utilisateur(self):
        util = get_identifiant_utilisateur(self.identifiant.data)
        if util is None:
            return None
        return util
    
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.idRole == -1:
            return redirect(url_for('home_admin'))
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/motDePasseOublie')
def mdp_oublie():
    """fonction de redirection vers la page de mot de passe oublié"""
    f = MdpOublieForm()
    return render_template('mdp_oublie.html', title='Mot de passe oublié', form = f)

@app.route('/motDePasseOublie/valider', methods=['POST'])
def valider_mdp_oublie():
    """fonction de validation de mot de passe oublié"""
    msg_erreur = ""
    f = MdpOublieForm()
    if f.validate_on_submit():
        if is_admin_identifiant(f.identifiant.data):
            msg_erreur = "Vous ne pouvez pas changer le mot de passe d'un administrateur"
        elif f.identifiant.data == "" or f.mdp.data == "" or f.mdpConfirm.data == "":
            msg_erreur = "Veuillez remplir tous les champs"
        elif is_identifant(f.identifiant.data) is None:
            msg_erreur = "L'identifiant n'existe pas"
        elif f.mdp.data == f.mdpConfirm.data:
            m = sha256()
            m.update(f.mdp.data.encode())
            mdp = m.hexdigest()
            util = f.get_authentification_utilisateur()
            util.mdp = mdp
            db.session.commit()
            return redirect(url_for('login'))
        else:
            msg_erreur = "Les mots de passe ne correspondent pas"
    return render_template('mdp_oublie.html', title='Mot de passe oublié', form = f, erreur = msg_erreur)

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
    return render_template('rechercheComptes.html', title='Gestion des comptes', users=get_utilisateurs(), casernes = get_casernes(), grades = get_grades(), selectGrade=selectGrade, selectCaserne=selectCaserne, searchNom=searchNom, util = informations_utlisateurs())


@app.route('/administrateur/modifierCompte/<id>', methods=['GET', 'POST'])
@login_required
def modifier_compte(id):
    """redirection vers la page de modification d'un compte"""
    if not is_admin():
        return redirect(url_for('home'))
    user = Utilisateur.query.get(id)
    if request.form.get('save_compte') =="Sauvegarder le compte":
        if request.form.get('pseudo') != user.identifiant and is_identifant(request.form.get('pseudo')):
            return render_template('modifierCompte.html', title='Modifier de Compte', user=user, grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs(), erreur = "L'identifiant existe déjà")
        user.nomUtilisateur = request.form.get('nom')
        user.prenomUtilisateur = request.form.get('prenom')
        user.identifiant = request.form.get('pseudo')
        if request.form.get('password') != "":
            user.mdp = sha256(request.form.get('password').encode()).hexdigest()
        user.idGrade = request.form.get('grades')
        user.idCas = request.form.get('casernes')
        user.idRole = request.form.get('roles')
        db.session.commit() 
        return redirect(url_for('recherche_comptes')) 
    return render_template('modifierCompte.html', title="Modification d'un compte", roles=get_roles(), user=user, grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs())

@app.route('/administrateur/rechercheDocAdmin')
@login_required
def recherche_doc_admin():
    """page de recherche des documents pour l'administrateur"""
    if not is_admin():
        return redirect(url_for('home'))
    global active_tags, selectType
    has_result = False
    result = []
    # document = get_documents()
    for i in get_types():
        resultat = dict()
        resultat["nomType"] = i.nomType
        resultat["element"] = []

        for document in get_document_types(i.idType, documents):
            resultat["element"].append(document)
            has_result = True
        result.append(resultat)
    return render_template("recherche_doc_admin.html",title="Gestion des documents", tags = get_tags(), active_tags = active_tags, result = result, types= get_types(), util = informations_utlisateurs(), selectType=selectType, search=filtre_texte, has_result = has_result)

@app.route('/administrateur/modifierDocument/<id>', methods=['GET', 'POST'])
def modifier_document(id):
    """fonction de modification de document"""
    if not is_admin():
        return redirect(url_for('home'))
    doc = get_document_id(id)
    if request.form.get('modifier_document') =="Enregistrer":
        doc.nomDoc = request.form.get('titre')
        doc.idType = request.form.get('types')
        doc.descriptionDoc = request.form.get('description')
        db.session.commit()
        global documents
        documents = []
        handle_filtrage(True)
        return redirect(url_for('recherche_doc_admin'))
    if request.form.get('annuler') =="Annuler":
        return redirect(url_for('recherche_doc_admin'))
    return render_template('modifier_document.html', title="Modification d'un document", doc=doc, types = get_types(), tags=get_tags(), util = informations_utlisateurs())


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
        newfile = request.files['file']
        if newfile.filename != "":
            if session.get('file') and session.get('file') != mkpath(os.path.join(app.config['UPLOAD_FOLDER'],"temporaire", filename)):
                os.remove(session.get('file'))
            file = request.files['file']
            filename = secure_filename(file.filename)
            session['file'] = mkpath(os.path.join(app.config['UPLOAD_FOLDER'],"temporaire", filename))
            file.save(session['file'])
        document = session.get('file').split("temporaire/")[-1]
        if request.form.get('generer-tag'):
            if session['file'] != "":
                tags_auto = generationTag(session['file'])
                for tag in tags_auto:
                    tag_manuel.add(tag)
            else:
                print("Aucun fichier n'a été sélectionné")
        if request.form.get('ajouter_document') =="Enregistrer":
            for tag in tag_manuel:
                if not get_tag_id(tag.idTag):
                    db.session.add(tag)
                    db.session.commit()
            file = request.files['file']
            if file.filename == "":
                filepath = session.get('file').split("temporaire/")[-1]
            else:
                filepath = secure_filename(file.filename)
            if request.form.get('type_document') != "Type": 
                type = request.form.get('type_document')
                nom_document = filepath.split("/")[-1]
                protection = request.form.get('niveau_document')
                if protection == "Niveau de protection":
                    protection = 1
                document = Document(
                    nomDoc = request.form.get('titre'),
                    idType = type or 1,
                    fichierDoc = filepath,
                    descriptionDoc = request.form.get('description'),
                    niveauProtection = protection
                )
                db.session.add(document)
                db.session.commit()
            shutil.move(session.get('file'), mkpath(os.path.join(app.config['UPLOAD_FOLDER'], filepath)))
            for tag in tag_manuel:
                document_tag = DocumentTag(
                    idDoc = document.idDoc,
                    idTag = tag.idTag
                )
                db.session.add(document_tag)
                db.session.commit()
            tag_manuel.clear()
            session['file'] = ""
            return redirect(url_for('recherche_doc_admin'))
        return render_template('ajouter_document.html', tags=get_tags(), roles = get_roles(),document = document, type =request.form.get('type_document'), util = informations_utlisateurs(),new_tag=tag_manuel,titre =request.form.get('titre'), description = request.form.get('description'), active_type = request.form.get('type_document'), repertoire = request.form.get('repertoire'),types = get_types(), title="Ajouter un document")
    else:
        session['file'] = ""
    return render_template('ajouter_document.html', types = get_types(), roles = get_roles(), type = "Type",titre ="", description = "", tags=get_tags(),new_tag=tag_manuel, util = informations_utlisateurs(), title="Ajouter un document")

@app.route('/administrateur/importerRepertoire', methods=['GET', 'POST'])
@login_required
def importer_repertoire():
    """fonction d'importation de répertoire"""
    if not is_admin():
        return redirect(url_for('home'))
    documents = []
    if request.method == 'POST':
        if request.form.get('ajouter_document') =="Enregistrer":
            files = request.files.getlist('files')
            for file in files:
                if file.filename != "":
                    filename = file.filename
                    path = filename.split("/")
                    pathfinal = ""
                    for i in range(len(path)-1):
                        pathfinal += path[i]+"/"
                        if not os.path.exists(mkpath(os.path.join(app.config['UPLOAD_FOLDER'], pathfinal))):
                            os.makedirs(mkpath(os.path.join(app.config['UPLOAD_FOLDER'], pathfinal)))
                    file.save(mkpath(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
                    nom_document = filename.split("/")[-1]
                    protection = request.form.get('niveau_document')
                    document = Document(
                        nomDoc = nom_document,
                        idType = request.form.get('type_document') or 1,
                        fichierDoc = filename,
                        descriptionDoc = "",
                        niveauProtection = request.form.get('niveau_document')
                    )
                    db.session.add(document)
                    db.session.commit()
                    tags = generationTagDossier(mkpath(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
                    print(tags)
                    for tag in tags:
                        print(tag.idTag)
                        document_tag = DocumentTag(
                            idDoc = document.idDoc,
                            idTag = tag.idTag
                        )
                        db.session.add(document_tag)
                        db.session.commit()
                    id_tag = request.form.get('tag_document')
                    if id_tag != "Choisir un Tag":
                        document_tag = DocumentTag(
                            idDoc = document.idDoc,
                            idTag = id_tag
                        )
                        db.session.add(document_tag)
                        db.session.commit()
                    documents.append(document)
                    document.nomType = get_type(document.idType).nomType
    return render_template('importer_repertoire.html', title='Importer un répertoire', util = informations_utlisateurs(), types = get_types(), tags=get_tags(), roles = get_roles(), documents = documents)

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

@app.route('/administrateur/appliquer_filtre_tags', methods=['GET', 'POST'])
@login_required
def ajouter_filtre_tag():
    """fonction d'ajout de filtre pour la recherche de tags"""
    if not is_admin():
        return redirect(url_for('home'))
    if request.form.get('reset'):
        return redirect(url_for('recherche_tags'))
    if request.method=='POST':
        tags_search = request.form.get('barre_recherche')
        tags = get_tags_nom(tags_search)
    return render_template('recherche_tags.html', title='Gestion des tags', util = informations_utlisateurs(), tags = tags)

@app.route('/administrateur/supprimerDoc/<id>')
@login_required
def supprimer_document(id):
    """fonction de suppression d'un document"""
    if not is_admin():
        return redirect(url_for('home'))
    supprimer_doctag_by_docid(id)
    supprimer_favoris_by_docid(id)
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
    id_role = SelectField('Role', choices = [])

@app.route('/administrateur/ajouteCompte')
@login_required
def ajoute_compte():
    """fonction d'ajoute de compte"""
    if not is_admin():
        return redirect(url_for('home'))
    f = AjouteCompteForm()
    f.id_grade.choices = [(g.idGrade, g.nomGrade) for g in get_grades()]
    f.id_caserne.choices = [(c.idCas, c.nomCaserne) for c in get_casernes()]
    f.id_role.choices = [(r.idRole, r.nomRole) for r in get_roles()]
    return render_template('ajoute_compte.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs(), title="Ajout d'un compte", form=f)

@app.route('/administrateur/supprimerCompte/<int:id>')
@login_required
def supprimer_compte(id):
    """fonction de suppression de compte"""
    if not is_admin():
        return redirect(url_for('home'))
    supprimer_favoris_by_userid(id)
    util = get_utilisateur(id)
    db.session.delete(util)
    db.session.commit()
    return redirect(url_for('recherche_comptes'))

@app.route("/administrateur/ajouteCompte/save", methods=["POST"])
def save_compte():
    """fonction d'enregistrement d'un nouveau compte"""
    msg_erreur = ""
    if not is_admin():
        return redirect(url_for('home'))
    form = AjouteCompteForm()
    form.id_grade.choices = [(g.idGrade, g.nomGrade) for g in get_grades()]
    form.id_caserne.choices = [(c.idCas, c.nomCaserne) for c in get_casernes()]
    form.id_role.choices = [(r.idRole, r.nomRole) for r in get_roles()]

    if form.validate_on_submit():
        if is_identifant(form.pseudo.data):
            return render_template('ajoute_compte.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs(), title='Ajouter un compte', form=form, erreur = "L'identifiant existe déjà")
        else:
            util = Utilisateur(
                idUtilisateur= max_id_utilisateur()+1,
                nomUtilisateur= form.nomUser.data,
                prenomUtilisateur= form.prenomUser.data,
                identifiant= form.pseudo.data,
                mdp= sha256(form.mdp.data.encode()).hexdigest(),
                idGrade= form.id_grade.data,
                idRole= form.id_role.data,
                idCas= form.id_caserne.data
            )
            db.session.add(util)
            db.session.commit()
            return redirect(url_for('recherche_comptes'))
    return render_template('ajoute_compte.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs(), title='Ajouter un compte', form=form)
  
@app.route('/administrateur/recherche_tags')
@login_required
def recherche_tags():
    if not is_admin():
        return redirect(url_for('home'))
    return render_template('recherche_tags.html', util = informations_utlisateurs(), title='Gestion des tags', tags = get_tags())

@app.route('/administrateur/supprimerTag/<id>')
@login_required
def supprimer_tag(id):
    if not is_admin():
        return redirect(url_for('home'))
    supprimer_doctag_by_doctag(id)
    liaisons_tag_docs = get_liaison_document_tag(id)
    for liaison in liaisons_tag_docs:
        db.session.delete(liaison)
    tag = get_tag_id(id)
    global active_tags
    if tag in active_tags:
        active_tags.remove(tag)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('recherche_tags'))

def handle_filtrage(admin=False, reload_fav=False):
    global active_tags, filtre_texte, documents, selectType, favoris, extension

    # Si on reset les filtres cela remet tout à vide
    if request.form.get('reset'):
        active_tags.clear()
        filtre_texte = ""
        documents = []
        if admin:
            selectType = "Choisir un type"
            return redirect(url_for('recherche_doc_admin'))
        extension = ""
        return redirect(url_for('home'))
    favoris_clicked = False

    # Si on interagit avec les favoris
    if reload_fav or request.form.get('favoris'):
        favoris_clicked = True
        if not reload_fav:
            favoris = not favoris
        documents = get_favoris_user(current_user.idUtilisateur)
        active_tags.clear()
        filtre_texte = ""
        extension = ""
        return redirect(url_for('home'))
    
    # Sinon, ou si on retire favoris
    if not favoris_clicked or not favoris:
        favoris = False
        tag = request.form.get('tags')
        bool_fulldoc = False
        # Cas qui demande le chargement de tous les documents
        if not documents:
            if admin:
                if not active_tags and not filtre_texte and selectType == "Choisir un type":
                    documents = get_documents()
                    bool_fulldoc = True
            else:
                if not filtre_texte:
                    documents = get_documents()
                    bool_fulldoc = True
        if extension != request.form.get('extensions') and request.form.get('extensions') != "Choisir une extension":
            documents = get_documents()
            bool_fulldoc = True
            if filtre_texte != "":
                documents = get_filtrer_document_nom(documents, filtre_texte)
        if not bool_fulldoc and filtre_texte == "" and filtre_texte != request.form.get('barre_recherche') and active_tags == set():
            documents = get_documents()
            bool_fulldoc = True
        if admin and not bool_fulldoc and selectType == "Choisir un type" and request.form.get(
                'types') != "Choisir un type":
            selectType = request.form.get('types')
            documents = get_documents()
            bool_fulldoc = True
        # Filtre par type
        elif admin:
            selectType = "Choisir un type"
        # Recherche par mot ou ajout tag par point
        if request.form.get('barre_recherche'):
            if request.form.get('barre_recherche')[0] != ".":
                filtre_texte = request.form.get('barre_recherche')
                documents = get_filtrer_document_nom(documents, filtre_texte)
            else:
                tag_barre = get_tag(request.form.get('barre_recherche')[1:], True)
                if not tag_barre or tag_barre in active_tags:
                    tag_barre = get_tag(request.form.get('barre_recherche')[1:])
                if tag_barre:
                    active_tags.add(tag_barre)
                    documents = get_filtrer_document_tag(documents, tag_barre)
        if request.form.get('extensions') is not None:
            extension = request.form.get('extensions')
            if extension != "Choisir une extension":
                documents = get_filtrer_document_extension(documents, extension)
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

        # Si il y a aucun critère de recherche, alors on load aucun document
        if admin:
            if not active_tags and not filtre_texte and selectType == "Choisir un type":
                documents = []
        else:
            if not active_tags and not filtre_texte:
                documents = []
        # permet de trier des documents par des tags
        for tag_act in active_tags:
            documents = get_filtrer_document_tag(documents, tag_act)

@app.route("/administrateur/gerer_compte/erreur")
@login_required
def erreur_compte():
    """fonction destinée à gérer les erreurs de connexion"""
    if not is_admin():
        return redirect(url_for('home'))


@app.route('/genererTag')
def genererTag():
    return "Tag généré"