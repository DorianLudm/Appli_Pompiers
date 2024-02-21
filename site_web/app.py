from flask_bootstrap import Bootstrap5
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os.path
from flask import request, jsonify, render_template

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname( __file__ ),p))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../BD/DB_Pompiers.db'))
db = SQLAlchemy(app)
app.config['BOOTSTRAP_SERVE_LOCAL']=True
bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = '94da14e7-22ba-424c-b262-f5eeb505e5e9'
app.config['UPLOAD_FOLDER'] = 'static/document'

login_manager = LoginManager(app)
login_manager.login_view = "login"

from .models import Tag

@app.route('/update-tag-color', methods=['POST'])
def update_tag_color_route():
    data = request.get_json()
    tag = Tag.query.get(data['id'])
    if tag:
        tag.couleurTag = data['color'][1:]
        db.session.commit()
    return '', 204

@app.route('/update-tag-name', methods=['POST'])
def update_tag_name_route():
    data = request.get_json()
    tag = Tag.query.get(data['id'])
    if tag:
        tag.nomTag = data['name']
        db.session.commit()
    return '', 204

from .views import active_tags, ajouter_filtre

@app.route('/add_active_tag', methods=['POST'])
def add_active_tag():
    data = request.get_json()
    selected_tag_name = data['tag']
    tags = Tag.query.all()
    for tag in tags:
        if tag.nomTag == selected_tag_name:
            selected_tag = tag
            break
    if selected_tag is None:
        return jsonify('Tag not found')
    active_tags.add(selected_tag)
    return jsonify()
