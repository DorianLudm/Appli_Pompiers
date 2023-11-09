from .app import app, mkpath
from flask import render_template, url_for , redirect, request,  flash, session
from .models import get_tags, get_types, get_document_id, get_document_types, get_tag_nom,get_tag, Utilisateur, get_identifiant_utilisateur, get_grades, get_casernes, informations_utlisateurs, get_utilisateurs
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user, logout_user, login_required
import webbrowser

active_tags = []
filtre_texte = ""

@app.route('/pompier')
@login_required
def home():
    global active_tags
    result = []
    for i in get_types():
        resultat = dict()
        resultat["nomType"] = i.nomType
        resultat["element"] = []
        
        for document in get_document_types(i.idType, active_tags,filtre_texte):
            resultat["element"].append(document)
        result.append(resultat)
    return render_template("recherche_doc.html",tags = get_tags(), active_tags = active_tags, result = result, util = informations_utlisateurs())
 
@app.route('/ajouter_filtre/', methods =("POST",))
def ajouter_filtre():
    print("FILTRE")
    global active_tags, filtre_texte
    if request.method=='POST':
        tag=request.form['tags']
        if tag != "Choisir un tag":
            active_tags.append(tag)
        if request.form.get('barre_recherche'):
            if request.form.get('barre_recherche')[0] != ".":
                filtre_texte = request.form.get('barre_recherche')   
            else:
                active_tags.append(get_tag(request.form.get('barre_recherche')[1:]))   
        if request.form.get('reset') == 'Reset':
            active_tags = []
            filtre_texte = ""
            return redirect(url_for('home'))
        elif request.form.get('retirer_filtre'):
            active_tags.remove(request.form.get('retirer_filtre'))
    return redirect(url_for('home'))


@app.route('/ouverture_doc/<id>', methods =("POST",))
def ouverture_doc(id):
    doc = get_document_id(id).fichierDoc
    webbrowser.open(mkpath('./static/document/' + doc)) 
    return redirect(url_for('home'))
  


# LOGIN

class LoginForm( FlaskForm ):
    identifiant = StringField('Identifiant')
    mdp = PasswordField('Password')
    def get_authentification_utilisateur(self):
        util = get_identifiant_utilisateur(self.identifiant.data)
        print(util)
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
            return redirect(url_for("home_admin"))
        else:
            print("probleme")
            return render_template(
                "login.html",
                form=f,
                erreur = "Login ou mot de passe incorrect")
    return render_template(
        "login.html",
        form=f)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))  

# ADMINISTRATION

@app.route('/administrateur')
@login_required
def home_admin():
  return render_template('accueil_admin.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs())

@app.route('/rechercheComptes')
def recherche_comptes(searchNom="", selectGrade="Choisir un grade", selectCaserne="Choisir une caserne"):
    print(searchNom+"1")
    return render_template('rechercheComptes.html', title='Recherche de comptes', users=get_utilisateurs(), casernes = get_casernes(), grades = get_grades(), 
                            selectGrade=selectGrade, selectCaserne=selectCaserne, searchNom=searchNom, util = informations_utlisateurs())
  

@app.route('/rechercheDocuments')
@login_required
def recherche_document():
    return render_template('rechercheDocuments.html')

@app.route('/administrateur/ajouteDocument')
@login_required
def ajoute_document():
    return render_template('ajouter_document.html', util = informations_utlisateurs())

@app.route('/appliquer_filtres', methods=['GET', 'POST'])
def appliquer_filtres():
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

@app.route('/administrateur/ajouteCompte')
@login_required
def ajoute_compte():
    return render_template('ajoute_compte.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs())

@app.route("/administrateur/gerer_compte/save")
def save_compte():
    try:
        return 1
    except:
        erreur_compte()

class CompteForm(FlaskForm):
    nomUser = StringField('Nom', validators = [DataRequired()])
    prenomUser = StringField('Prenom', validators = [DataRequired()])
    pseudo = StringField("Nom d'utilisateur", validators = [DataRequired()])
    mdp = PasswordField('Mot de passe', validators = [DataRequired()])
    grade_id = IntegerField('ID Grade', validators = [DataRequired()])
    caserne_id = IntegerField('ID Caserne', validators = [DataRequired()])
    # chef = bool('Est chef de caserne', validators = [DataRequired()])

@app.route("/administrateur/gerer_compte/erreur")
def erreur_compte():
    # Faire un pop-up d'erreur (?)
    print("erreur")
