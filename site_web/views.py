from .app import app
from flask import render_template, request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from .models import Utilisateur, get_identifiant_utilisateur, get_grades, get_casernes, informations_utlisateurs, get_utilisateurs
from hashlib import sha256
from flask_login import login_user, logout_user, login_required


@app.route('/administrateur')
@login_required
def home():
    return render_template('accueil_admin.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs())

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
            return redirect(url_for("home"))
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

@app.route('/rechercheComptes')
def recherche_comptes(searchNom="", selectGrade="Choisir un grade", selectCaserne="Choisir une caserne"):
    print(searchNom+"1")
    return render_template('rechercheComptes.html', title='Recherche de comptes', users=get_utilisateurs(), casernes = get_casernes(), grades = get_grades(), 
                            selectGrade=selectGrade, selectCaserne=selectCaserne, searchNom=searchNom, util = informations_utlisateurs())

@app.route('/rechercheDocuments')
@login_required
def recherche_document():
    return render_template('rechercheDocuments.html')

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

@app.route('/administrateur/ajoutCompte')
@login_required
def ajout_compte():
    return render_template('ajout_compte.html', grades = get_grades(), casernes = get_casernes(), util = informations_utlisateurs())
