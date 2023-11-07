import click
from .app import app, db
from .models import Utilisateur
from hashlib import sha256

@app.cli.command()
def initdb():
    """Crée la base de données """
    db.create_all()
    click.echo('Initialisation de la base de données')

@app.cli.command()
def newuser():
    """Crée un nouvel utilisateur """
    identifiant = input("Identifiant : ")
    mdp = sha256(input("Mot de passe : ").encode()).hexdigest()
    util = Utilisateur(identifiant, mdp)
    db.session.add(util)
    db.session.commit()
    click.echo('Utilisateur créé')