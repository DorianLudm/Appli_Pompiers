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

active_tags = set()
filtre_texte = ""
selectType = "Choisir un type"

@app.route('/pompier')
@login_required
def home():
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
    return render_template("recherche_doc.html",tags = get_tags(), active_tags = active_tags, result = result, util = informations_utlisateurs(), title='Accueil',doc = doc)
 
@app.route('/ajouter_filtre/', methods =("POST",))
@login_required
def ajouter_filtre():
    global active_tags, filtre_texte, documents
    if not documents:
        if not active_tags and not filtre_texte:
            documents = get_documents()
    if request.method=='POST':
        tag=request.form['tags']
        if tag != "Choisir un tag":
            tag = get_tag(request.form.get('tags'))
            if tag:
                active_tags.add(tag)
                documents = get_filtrer_document_tag(documents, tag)
        if request.form.get('barre_recherche'):
            if request.form.get('barre_recherche')[0] != ".":
                filtre_texte = request.form.get('barre_recherche')   
                documents = get_filtrer_document_nom(documents, filtre_texte)
            else:
                tag = get_tag(request.form.get('barre_recherche')[1:])
                if tag:
                    active_tags.add(tag)
                    documents = get_filtrer_document_tag(documents, tag)
        if request.form.get('reset') == 'Reset':
            active_tags = set()
            filtre_texte = ""
            return redirect(url_for('home'))
        elif request.form.get('retirer_filtre'):
            tag_supprimer = None
            for tag in active_tags:
                if tag.nomTag == request.form.get('retirer_filtre'):
                    tag_supprimer = tag
            if tag_supprimer:
                active_tags.remove(tag_supprimer)
                
            documents = get_documents()
            if filtre_texte:
                documents = get_filtrer_document_nom(documents, filtre_texte)
            for tag in active_tags:
                documents = get_filtrer_document_tag(documents, tag)
                
                
    return redirect(url_for('home'))

@app.route('/ouverture_doc/<id>', methods =("POST",))
@login_required
def ouverture_doc(id):
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
    logout_user()
    return redirect(url_for('login'))  

# ADMINISTRATION
@app.route('/administrateur')
def home_admin():
    if not is_admin():
        return redirect(url_for('home'))
    return render_template('accueil_admin.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs(), title='Acceuil administrateur')

@app.route('/administrateur/rechercheComptes')
@login_required
def recherche_comptes(searchNom="", selectGrade="Choisir un grade", selectCaserne="Choisir une caserne"):
    if not is_admin():
        return redirect(url_for('home'))
    return render_template('rechercheComptes.html', title='Recherche de comptes', users=get_utilisateurs(), casernes = get_casernes(), grades = get_grades(), 
                            selectGrade=selectGrade, selectCaserne=selectCaserne, searchNom=searchNom, util = informations_utlisateurs())

@app.route('/gerer_tags')
@login_required
def gerer_tags():
    return render_template('gerer_tags.html')

@app.route('/administrateur/modifierCompte/<id>', methods=['GET', 'POST'])
@login_required
def modifier_compte(id):
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
    if not is_admin():
        return redirect(url_for('home'))
    global active_tags, selectType
    result = []
    for i in get_types():
        resultat = dict()
        resultat["nomType"] = i.nomType
        resultat["element"] = []
        
        for document in get_document_types(i.idType, active_tags,filtre_texte):
            resultat["element"].append(document)
        result.append(resultat)
    return render_template("recherche_doc_admin.html",title="Admin | Recherche documents", tags = get_tags(), active_tags = active_tags, result = result, types= get_types(), util = informations_utlisateurs(), selectType=selectType, search=filtre_texte)

@app.route('/administrateur/modifierDocument/<id>', methods=['GET', 'POST'])
def modifier_document(id):
    if not is_admin():
        return redirect(url_for('home'))
    doc = get_document_id(id)
    if request.form.get('modifier_document') =="Enregistrer":
        doc.nomDoc = request.form.get('titre')
        doc.idType = request.form.get('types')
        db.session.commit()
        return redirect(url_for('recherche_doc_admin')) 
    if request.form.get('annuler') =="Annuler":
        return redirect(url_for('recherche_doc_admin'))
    return render_template('modifier_document.html', title='Modifier de Document', doc=doc, types = get_types(), tags=get_tags(), util = informations_utlisateurs())

@app.route('/administrateur/ajouteDocument')
@login_required
def ajoute_document():
    if not is_admin():
        return redirect(url_for('home'))
    return render_template('ajouter_document.html', util = informations_utlisateurs(), title='Ajouter un document')

@app.route('/administrateur/appliquer_filtres', methods=['GET', 'POST'])
@login_required
def appliquer_filtres():
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
    if not is_admin():
        return redirect(url_for('home'))
    global active_tags, filtre_texte, selectType
    if request.method=='POST':
        filtre_texte = request.form.get('barre_recherche')
        selectType = request.form.get('types')
        if selectType == "Tous les types":
            selectType = "Choisir un type"
        tag=request.form['tags']
        if tag != "Choisir un tag":
            tag = get_tag(request.form.get('tags')[1:])
            active_tags.add(tag)
        if request.form.get('barre_recherche'):
            if request.form.get('barre_recherche')[0] != ".":
                filtre_texte = request.form.get('barre_recherche')   
            else:
                active_tags.add(get_tag(request.form.get('barre_recherche')[1:]))   
        if request.form.get('reset'):
            active_tags = []
            filtre_texte = ""
            selectType = "Choisir un type"
            return redirect(url_for('recherche_doc_admin'))
        elif request.form.get('retirer_filtre'):
            for tag in active_tags:
                if tag.nomTag == request.form.get('retirer_filtre'):
                    active_tags.remove(tag)
    return redirect(url_for('recherche_doc_admin'))

@app.route('/administrateur/supprimerDoc/<id>')
@login_required
def supprimer_document(id):
    if not is_admin():
        return redirect(url_for('home'))
    document = get_document_id(id)
    db.session.delete(document)
    db.session.commit()
    return ajouter_filtre_doc_admin()

class AjouteCompteForm(FlaskForm):
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
    if not is_admin():
        return redirect(url_for('home'))
    f = AjouteCompteForm()
    f.id_grade.choices = [(g.idGrade, g.nomGrade) for g in get_grades()]
    f.id_caserne.choices = [(c.idCas, c.nomCaserne) for c in get_casernes()]
    return render_template('ajoute_compte.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs(), title='Ajouter un compte', form=f)

@app.route('/administrateur/supprimerCompte/<id>')
@login_required
def supprimer_compte(id):
    if not is_admin():
        return redirect(url_for('home'))
    util = get_utilisateur(id)
    db.session.delete(util)
    db.session.commit()
    return appliquer_filtres()


@app.route("/administrateur/ajouteCompte/save", methods=["POST"])
def save_compte():
    if not is_admin():
        return redirect(url_for('home'))
    form = AjouteCompteForm()
    form.id_grade.choices = [(g.idGrade, g.nomGrade) for g in get_grades()]
    form.id_caserne.choices = [(c.idCas, c.nomCaserne) for c in get_casernes()]

    if form.validate_on_submit():
        if form.id_role.data:
            role = -1
        role = 2
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



@app.route("/administrateur/gerer_compte/erreur")
@login_required
def erreur_compte():
    if not is_admin():
        return redirect(url_for('home'))
    # Faire un pop-up d'erreur (?)
    print("erreur")