from .app import app
from flask import render_template

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rechercheDocuments')
def recherche_document():
    return render_template('rechercheDocuments.html')