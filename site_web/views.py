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
    return render_template("recherche_doc.html",tags = tags, active_tags = tags)