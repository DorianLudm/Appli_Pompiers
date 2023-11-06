from .app import app, mkpath
from flask import render_template
from .models import get_tags, get_types
import webbrowser

@app.route('/')
def home():
    result = []
    for i in get_types():
        resultat = dict()
        resultat["nomType"] = i.nomType
        resultat["element"] = []
        for j in range(4):
            element = dict()
            element["nomDoc"] = "element"+str(j)
            resultat["element"].append(element)
        result.append(resultat)
    webbrowser.open(mkpath('../'))
    return render_template("recherche_doc.html",tags = get_tags(), active_tags = get_tags(), result = result)

@app.route('/login')
def login():
    return render_template('login.html')
