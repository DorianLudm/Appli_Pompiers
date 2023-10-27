from .app import app
from flask import render_template

@app.route('/')
def home():
    tags = []
    for i in range(3):
        tag = dict()
        tag["nom"] = "tag"+str(i)
        print(tag)
        tags.append(tag) 
    result = []
    for i in range(4):
        resultat = dict()
        resultat["nom"] = "resultat"+str(i)
        resultat["element"] = []
        print(resultat)
        for j in range(4+i):
            element = dict()
            element["nom"] = "element"+str(j)
            resultat["element"].append(element)
        result.append(resultat)
    return render_template("recherche_doc.html",tags = tags, active_tags = tags, result = result)