from .app import app
from flask import render_template, request
from .models import get_utilisateurs, get_grades, get_casernes

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rechercheComptes')
def recherche_comptes(selectGrade="Choisir un grade", selectCaserne="Choisir une caserne"):
    return render_template('rechercheComptes.html', title='Recherche de comptes', users=get_utilisateurs(), casernes = get_casernes(), grades = get_grades(), selectGrade=selectGrade, selectCaserne=selectCaserne)

@app.route('/rechercheDocuments')
def recherche_document():
    return render_template('rechercheDocuments.html')

@app.route('/appliquer_filtres', methods=['GET', 'POST'])
def appliquer_filtres():
    if request.method == 'POST':
        if "appliquer" in request.form:
            selectGrade = request.form.get('grades')
            selectCaserne = request.form.get('casernes')
            return recherche_comptes(selectGrade, selectCaserne)
    return recherche_comptes()