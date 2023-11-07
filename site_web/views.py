from .app import app
from flask import render_template
# Cet import est un test
from .models import get_grades, get_caserne

@app.route('/')
def home():
    return render_template('ajout_compte.html', grades = get_grades(), casernes = get_caserne())

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rechercheDocuments')
def recherche_document():
    return render_template('rechercheDocuments.html')