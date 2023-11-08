from .app import app, mkpath
from flask import render_template, url_for , redirect, request
from .models import get_tags, get_types, get_document_id, get_document_types, get_tag_nom
from flask_wtf import FlaskForm
from wtforms import StringField
import webbrowser

active_tags = []
filtre_texte = ""

@app.route('/')
def home():
    global active_tags
    result = []
    for i in get_types():
        resultat = dict()
        resultat["nomType"] = i.nomType
        resultat["element"] = []
        
        for document in get_document_types(i.idType, active_tags):
            resultat["element"].append(document)
        result.append(resultat)
    return render_template("recherche_doc.html",tags = get_tags(), active_tags = active_tags, result = result)
 
@app.route('/ajouter_filtre/', methods =("POST",))
def ajouter_filtre():
    if request.method=='POST':
        tag=request.form['tags']
        name =request.form['name']
        if tag != "Choisir un tag":
            active_tags.append(tag)
        if name != "":
            print(name)
    return redirect(url_for('home'))

@app.route('/ouverture_doc/<id>', methods =("POST",))
def ouverture_doc(id):
    doc = get_document_id(id).fichierDoc
    webbrowser.open(mkpath('./static/document/' + doc)) 
    return redirect(url_for('home'))

@app.route('/login')
def login():
    return render_template('login.html')
