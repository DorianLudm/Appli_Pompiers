from .app import app
from flask import render_template, request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from .models import Utilisateur
from hashlib import sha256
from flask_login import login_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('base.html')

# -------------------------------------
# -                                   -
# -                                   -
# -              LOGIN                -
# -                                   -
# -                                   -
# -------------------------------------

class LoginForm( FlaskForm ):
    identifiant = StringField('Identifiant ')
    mdp = PasswordField('Password')
    def get_authentification_utilisateur(self):
        util = Utilisateur.query.get(self.identifiant.data)
        if util is None:
            return None
        m = sha256()
        m.update(self.mdp.data.encode())
        mdp = m.hexdigest()
        if mdp == util.mdp:
            return util
        else:
            return None

@app.route('/login', methods=['GET', 'POST'])
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

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))

# -------------------------------------
# -          FIN LOGIN                -
# -------------------------------------

@app.route('/rechercheDocuments')
def recherche_document():
    return render_template('rechercheDocuments.html')