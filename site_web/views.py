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
def recherche_comptes(searchNom="", selectGrade="Choisir un grade", selectCaserne="Choisir une caserne"):
    print(searchNom+"1")
    return render_template('rechercheComptes.html', title='Recherche de comptes', users=get_utilisateurs(), casernes = get_casernes(), grades = get_grades(), selectGrade=selectGrade, selectCaserne=selectCaserne, searchNom=searchNom)

@app.route('/rechercheDocuments')
def recherche_document():
    return render_template('rechercheDocuments.html')

@app.route('/appliquer_filtres', methods=['GET', 'POST'])
def appliquer_filtres():
    if request.method == 'POST':
        if "appliquer" in request.form:
            selectGrade = request.form.get('grades')
            selectCaserne = request.form.get('casernes')
            search_bar_value = request.form.get('search_bar')
            if selectGrade == "Tous les grades":
                selectGrade = "Choisir un grade"
            if selectCaserne == "Toutes les casernes":
                selectCaserne = "Choisir une caserne"
            return recherche_comptes(search_bar_value, selectGrade, selectCaserne)
        if "reset" in request.form:
            return recherche_comptes()
        search_bar_value = request.form.get('search_bar')
        return recherche_comptes(search_bar_value)
    return recherche_comptes()