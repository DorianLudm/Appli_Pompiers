from .app import app
from flask import render_template
from .models import get_utilisateurs, get_grades, get_casernes

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rechercheComptes')
def recherche_comptes():
    return render_template('rechercheComptes.html', title='Recherche de comptes', users=get_utilisateurs(), casernes = get_casernes(), grades = get_grades())

@app.route('/rechercheDocuments')
def recherche_document():
    return render_template('rechercheDocuments.html')
